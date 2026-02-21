import pandas as pd

class IADashboardExporter:

    def __init__(self, service):
        self.service = service

    def exportar(self, caminho: str):
        leads = self.service.lead_repo.consultar()

        linhas = []

        for lead in leads:
            lead_nome = getattr(lead, "nome", f"Lead {lead.id}")

            best = self.service.ia_repo.list_best(lead.id, 1)
            all_scores = self.service.ia_repo.list_by_lead(lead.id)

            # Caso não tenha nenhum imóvel avaliado
            if not all_scores:
                linhas.append({
                    "lead_id": lead.id,
                    "lead_nome": lead_nome,
                    "melhor_property_id": None,
                    "melhor_property_nome": None,
                    "melhor_score": 0,
                    "status": "SEM DADOS",
                    "imoveis_avaliados": 0,
                    "score_medio": 0
                })
                continue

            best_score = best[0].conversion_score if best else 0
            best_prop_id = best[0].property_id if best else None

            # Buscar nome do empreendimento
            prop = self.service.property_repo.find_by_id(best_prop_id)
            prop_nome = getattr(prop, "nome", f"Imóvel {best_prop_id}")

            avg = sum(r.conversion_score for r in all_scores) / len(all_scores)

            # STATUS
            if best_score >= 40:
                status = "ALTA"
            elif best_score >= 20:
                status = "MEDIA"
            else:
                status = "BAIXA"

            linhas.append({
                "lead_id": lead.id,
                "lead_nome": lead_nome,
                "melhor_property_id": best_prop_id,
                "melhor_property_nome": prop_nome,
                "melhor_score": round(best_score, 2),
                "status": status,
                "imoveis_avaliados": len(all_scores),
                "score_medio": round(avg, 2)
            })

        df = pd.DataFrame(linhas)
        df.to_excel(caminho, index=False)

        return caminho
