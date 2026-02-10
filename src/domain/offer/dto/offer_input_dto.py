class OfferInputDTO:
    def __init__(
        self,
        lead_id: int,
        empreendimento_id: int,
        score: float,
        rationale: str
    ):
        self.lead_id = lead_id
        self.empreendimento_id = empreendimento_id
        self.score = score
        self.rationale = rationale
