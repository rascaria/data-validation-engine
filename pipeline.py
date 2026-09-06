import os
import pandas as pd
import validation_config as v

class SimpleReport:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.raw_df: pd.DataFrame | None = None
        self.cleaned_df: pd.DataFrame | None = None
        self.summary_df: pd.DataFrame | None = None

    def load_data(self):
        try:
            self.raw_df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")

    def clean_data(self):
        if self.raw_df is None:
            print("Cannot clean data, raw_df is not loaded.")
            return
        self.cleaned_df = self.raw_df.copy()
        # By converting to uppercase first, the mapping becomes simpler and more robust.
        self.cleaned_df['Hersteller_Clean'] = self.cleaned_df['Hersteller'].str.upper().str.strip()
        self.cleaned_df['Hersteller_Clean'] = self.cleaned_df['Hersteller_Clean'].replace(v.MANUFACTURER_MAPPING)

    def validate_data(self):
        if self.cleaned_df is not None:
            failure_masks = []
            for rule_name, rule_function in v.RULES.items():
                # A rule function returns True for every row that FAILS the rule.
                failure_mask = rule_function(self.cleaned_df)
                # Store the failure mask in its own column for detailed reporting.
                self.cleaned_df[f'failed_{rule_name}'] = failure_mask
                failure_masks.append(failure_mask)
            
            # Combine all failure masks. A row is invalid if it fails ANY rule.
            # We use `pd.concat` and `.any(axis=1)` to check for True in any of the failure columns for each row.
            combined_failures = pd.concat(failure_masks, axis=1)
            # A row is valid if it did NOT fail any rule.
            self.cleaned_df['is_valid'] = ~combined_failures.any(axis=1)

    def analyze_data(self):
        if self.cleaned_df is None:
            print("Cannot analyze data, cleaned_df is not available.")
            return
        # Filter for valid rows before performing the analysis.
        valid_df = self.cleaned_df[self.cleaned_df['is_valid']].copy()
        self.summary_df = valid_df.groupby('Hersteller_Clean').agg(total_num=('Anzahl', 'sum')).sort_values(by='total_num', ascending=False).reset_index()

    def run(self):
        self.load_data()
        self.clean_data()
        self.validate_data()
        self.analyze_data()

    def show_cleaned_data(self):
        """Helper method to display the intermediate cleaned data for debugging."""
        if self.cleaned_df is not None:
            print("\n--- Cleaned & Validated Data ---")
            print(self.cleaned_df.to_string(index=False))

    def show_summary(self):
        if self.summary_df is not None:
            print("\n--- Final Summary ---")
            print(self.summary_df.to_string(index=False))
        else:
            print("\nNo summary to show. Did the report run correctly?")

if __name__ == '__main__':
    # This creates a path to 'sample_fleet_data.csv'
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'sample_fleet_data.csv')
    
    report = SimpleReport(file_path)
    report.run()
    # report.show_cleaned_data()
    report.show_summary()