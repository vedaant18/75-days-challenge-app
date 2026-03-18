from app.extensions import ma
from app.models.proof import Proof


class ProofSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Proof
        load_instance = True

    status = ma.String()


proof_schema = ProofSchema()
proofs_schema = ProofSchema(many=True)
