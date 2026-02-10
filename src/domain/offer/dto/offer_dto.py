class OfferDTO:
    def __init__(
        self,
        id: int,
        lead_id: int,
        empreendimento_id: int,
        score: float,
        rationale: str,
        created_at: str
    ):
        self.id = id
        self.lead_id = lead_id
        self.empreendimento_id = empreendimento_id
        self.score = score
        self.rationale = rationale
        self.created_at = created_at
