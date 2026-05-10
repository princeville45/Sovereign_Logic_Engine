class ROIEngine:
    def __init__(self, sales_units, scripts_built, study_hours):
        self.sales = (sales_units / 250) * 0.3
        self.equity = (scripts_built / 8) * 0.4
        self.knowledge = (study_hours / 4) * 0.3

    def get_success_index(self):
        index = (self.sales + self.equity + self.knowledge) * 10
        return f\"Global ROI Index: {round(index, 1)}/10\"
