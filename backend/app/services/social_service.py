from sqlalchemy import select
from app.extensions import db
from app.models.user import User
from app.models.challenge import Challenge
from app.models.daily_log import DailyLog
from app.models.social import Follow, SharedUpdate
from app.utils.enums import SharedUpdateType, ChallengeStatus, DailyLogStatus
from app.utils.errors import NotFoundError, ConflictError, ValidationError


class SocialService:

    @staticmethod
    def get_public_profile(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise NotFoundError("User not found")
        if user.profile and not user.profile.is_public:
            raise NotFoundError("Profile is private")
        return user

    @staticmethod
    def get_full_profile(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            raise NotFoundError("User not found")
        if user.profile and not user.profile.is_public:
            raise NotFoundError("Profile is private")

        profile = user.profile

        # Followers / following counts
        followers_count = Follow.query.filter_by(followed_id=user.id).count()
        following_count = Follow.query.filter_by(follower_id=user.id).count()

        # All challenges
        challenges = Challenge.query.filter_by(user_id=user.id).order_by(
            Challenge.created_at.desc()
        ).all()

        challenge_cards = []
        for c in challenges:
            completed_days = DailyLog.query.filter_by(
                challenge_id=c.id, status=DailyLogStatus.COMPLETED
            ).count()
            challenge_cards.append({
                "id": c.id,
                "title": c.title,
                "description": c.description or "",
                "difficulty": c.difficulty.value,
                "status": c.status.value,
                "current_day": c.current_day,
                "total_days": c.total_days,
                "completed_days": completed_days,
                "start_date": c.start_date.isoformat() if c.start_date else None,
                "end_date": c.end_date.isoformat() if c.end_date else None,
            })

        # Daily activity heatmap — all daily logs across all challenges
        all_logs = DailyLog.query.join(Challenge).filter(
            Challenge.user_id == user.id
        ).order_by(DailyLog.date.asc()).all()

        heatmap = {}
        for log in all_logs:
            date_str = log.date.isoformat()
            heatmap[date_str] = {
                "status": log.status.value,
                "tasks_completed": log.tasks_completed,
                "tasks_total": log.tasks_total,
            }

        # Recent activity
        recent_updates = SharedUpdate.query.filter_by(
            user_id=user.id, is_public=True
        ).order_by(SharedUpdate.created_at.desc()).limit(10).all()

        activity = []
        for u in recent_updates:
            activity.append({
                "id": u.id,
                "type": u.update_type.value,
                "content": u.content,
                "day_number": u.day_number,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            })

        # Stats
        completed_challenges = sum(1 for c in challenges if c.status == ChallengeStatus.COMPLETED)
        total_completed_days = sum(
            1 for log in all_logs if log.status == DailyLogStatus.COMPLETED
        )

        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            },
            "profile": {
                "display_name": profile.display_name if profile else None,
                "bio": profile.bio if profile else None,
                "avatar_url": profile.avatar_url if profile else None,
                "is_public": profile.is_public if profile else True,
                "current_streak": profile.current_streak if profile else 0,
                "longest_streak": profile.longest_streak if profile else 0,
            },
            "stats": {
                "total_challenges": len(challenges),
                "completed_challenges": completed_challenges,
                "active_challenge": any(c.status == ChallengeStatus.ACTIVE for c in challenges),
                "total_completed_days": total_completed_days,
                "followers": followers_count,
                "following": following_count,
            },
            "challenges": challenge_cards,
            "heatmap": heatmap,
            "activity": activity,
        }

    @staticmethod
    def create_update(user_id, data):
        try:
            update_type = SharedUpdateType(data["update_type"].lower())
        except ValueError:
            raise ValidationError("Invalid update type")

        update = SharedUpdate(
            user_id=user_id,
            challenge_id=data.get("challenge_id"),
            update_type=update_type,
            content=data.get("content", ""),
            day_number=data.get("day_number"),
        )
        db.session.add(update)
        db.session.commit()
        return update

    @staticmethod
    def get_feed(user_id, page=1, per_page=20):
        following_ids = db.session.query(Follow.followed_id).filter(
            Follow.follower_id == user_id
        ).scalar_subquery()

        return SharedUpdate.query.filter(
            SharedUpdate.user_id.in_(following_ids),
            SharedUpdate.is_public.is_(True),
        ).order_by(
            SharedUpdate.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False).items

    @staticmethod
    def follow(user_id, target_user_id):
        if user_id == target_user_id:
            raise ValidationError("Cannot follow yourself")

        target = User.query.get(target_user_id)
        if not target:
            raise NotFoundError("User not found")

        existing = Follow.query.filter_by(
            follower_id=user_id, followed_id=target_user_id
        ).first()
        if existing:
            raise ConflictError("Already following this user")

        follow = Follow(follower_id=user_id, followed_id=target_user_id)
        db.session.add(follow)
        db.session.commit()

    @staticmethod
    def unfollow(user_id, target_user_id):
        follow = Follow.query.filter_by(
            follower_id=user_id, followed_id=target_user_id
        ).first()
        if not follow:
            raise NotFoundError("Not following this user")

        db.session.delete(follow)
        db.session.commit()
