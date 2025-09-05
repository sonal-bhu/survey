#!/usr/bin/env python3
"""
WISDOM Survey Data Analysis Tool
Analyzes responses from the WISDOM questionnaire and generates statistical reports.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import os
from datetime import datetime
from pathlib import Path

class WisdomAnalyzer:
    def __init__(self, data_file=None):
        """Initialize the analyzer with data file"""
        self.data_file = data_file or 'wisdom_survey_results.csv'
        self.df = None
        self.results = {}
        
    def load_data(self):
        """Load survey data from CSV file"""
        try:
            if os.path.exists(self.data_file):
                self.df = pd.read_csv(self.data_file)
                print(f"Loaded {len(self.df)} responses from {self.data_file}")
                return True
            else:
                print(f"Data file {self.data_file} not found.")
                print("Make sure to run the survey and collect some responses first.")
                return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def load_json_data(self, json_folder='survey_responses'):
        """Load individual JSON responses and combine into DataFrame"""
        json_files = list(Path(json_folder).glob('*.json')) if os.path.exists(json_folder) else []
        
        if not json_files:
            print(f"No JSON files found in {json_folder}/")
            return False
        
        data_list = []
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    data_list.append(data)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        if data_list:
            self.df = pd.DataFrame(data_list)
            print(f"Loaded {len(self.df)} responses from JSON files")
            return True
        
        return False
    
    def basic_statistics(self):
        """Calculate basic descriptive statistics"""
        if self.df is None:
            print("No data loaded. Please load data first.")
            return
        
        print("\n" + "="*60)
        print("BASIC DESCRIPTIVE STATISTICS")
        print("="*60)
        
        # Sample characteristics
        print(f"\nSample Size: {len(self.df)}")
        
        if 'age' in self.df.columns:
            age_data = pd.to_numeric(self.df['age'], errors='coerce').dropna()
            if not age_data.empty:
                print(f"Age Range: {age_data.min():.0f} - {age_data.max():.0f} years")
                print(f"Mean Age: {age_data.mean():.1f} ± {age_data.std():.1f} years")
        
        if 'gender' in self.df.columns:
            gender_counts = self.df['gender'].value_counts()
            if not gender_counts.empty:
                print(f"\nGender Distribution:")
                for gender, count in gender_counts.items():
                    if pd.notna(gender) and gender.strip():
                        print(f"  {gender}: {count} ({count/len(self.df)*100:.1f}%)")
        
        # Score statistics
        score_columns = ['total_wisdom_score', 'average_wisdom_score', 
                        'creativity_score', 'curiosity_score', 
                        'judgment_score', 'social_wisdom_score']
        
        available_scores = [col for col in score_columns if col in self.df.columns]
        
        if available_scores:
            print(f"\nSCORE STATISTICS:")
            print("-" * 50)
            
            stats_df = self.df[available_scores].describe()
            print(stats_df.round(2))
            
            # Store results
            self.results['basic_stats'] = stats_df.to_dict()
            self.results['sample_size'] = len(self.df)
            
        return self.results
    
    def correlation_analysis(self):
        """Analyze correlations between subscales"""
        if self.df is None:
            return
        
        score_columns = ['total_wisdom_score', 'creativity_score', 'curiosity_score', 
                        'judgment_score', 'social_wisdom_score']
        available_scores = [col for col in score_columns if col in self.df.columns]
        
        if len(available_scores) > 1:
            print(f"\nCORRELATION ANALYSIS:")
            print("-" * 50)
            
            corr_matrix = self.df[available_scores].corr()
            print(corr_matrix.round(3))
            
            self.results['correlations'] = corr_matrix.to_dict()
            
            # Create correlation heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, fmt='.3f')
            plt.title('WISDOM Subscale Correlations')
            plt.tight_layout()
            plt.savefig('wisdom_correlations.png', dpi=300, bbox_inches='tight')
            print(f"\nCorrelation heatmap saved as 'wisdom_correlations.png'")
            
        return self.results
    
    def reliability_analysis(self):
        """Calculate Cronbach's alpha for internal consistency"""
        if self.df is None:
            return
        
        print(f"\nRELIABILITY ANALYSIS:")
        print("-" * 50)
        
        # Get individual question responses
        q_columns = [col for col in self.df.columns if col.startswith('Q') and col.endswith('_numeric')]
        
        if len(q_columns) >= 20:
            # Overall scale reliability
            q_data = self.df[q_columns].dropna()
            
            if len(q_data) > 1:
                alpha_total = self.cronbach_alpha(q_data)
                print(f"Overall Scale Cronbach's α = {alpha_total:.3f}")
                
                # Subscale reliability
                subscales = {
                    'Creativity': [f'Q{i}_numeric' for i in [1, 6, 11, 16]],
                    'Curiosity': [f'Q{i}_numeric' for i in [2, 4, 7, 9, 12, 14, 17, 19]],
                    'Judgment': [f'Q{i}_numeric' for i in [3, 8, 13, 18]],
                    'Social Wisdom': [f'Q{i}_numeric' for i in [5, 10, 15, 20]]
                }
                
                print(f"\nSubscale Reliability:")
                reliability_results = {'total': alpha_total}
                
                for subscale_name, items in subscales.items():
                    available_items = [item for item in items if item in self.df.columns]
                    if len(available_items) > 1:
                        subscale_data = self.df[available_items].dropna()
                        if len(subscale_data) > 1:
                            # Reverse score Q2 for curiosity subscale
                            if subscale_name == 'Curiosity' and 'Q2_numeric' in available_items:
                                subscale_data_adj = subscale_data.copy()
                                subscale_data_adj['Q2_numeric'] = 6 - subscale_data_adj['Q2_numeric']
                                alpha = self.cronbach_alpha(subscale_data_adj)
                            else:
                                alpha = self.cronbach_alpha(subscale_data)
                            
                            print(f"  {subscale_name}: α = {alpha:.3f}")
                            reliability_results[subscale_name.lower().replace(' ', '_')] = alpha
                
                self.results['reliability'] = reliability_results
        
        return self.results
    
    def cronbach_alpha(self, df):
        """Calculate Cronbach's alpha"""
        try:
            # Number of items
            k = df.shape[1]
            
            # Variance of each item
            item_variances = df.var(axis=0, ddof=1)
            
            # Total variance
            total_variance = df.sum(axis=1).var(ddof=1)
            
            # Cronbach's alpha
            alpha = (k / (k - 1)) * (1 - item_variances.sum() / total_variance)
            
            return alpha
        except:
            return np.nan
    
    def generate_plots(self):
        """Generate visualization plots"""
        if self.df is None:
            return
        
        score_columns = ['total_wisdom_score', 'creativity_score', 'curiosity_score', 
                        'judgment_score', 'social_wisdom_score']
        available_scores = [col for col in score_columns if col in self.df.columns]
        
        if not available_scores:
            return
        
        # Distribution plots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, score in enumerate(available_scores):
            if i < len(axes):
                self.df[score].hist(bins=20, ax=axes[i], edgecolor='black', alpha=0.7)
                axes[i].set_title(f'{score.replace("_", " ").title()} Distribution')
                axes[i].set_xlabel('Score')
                axes[i].set_ylabel('Frequency')
        
        # Hide empty subplots
        for j in range(len(available_scores), len(axes)):
            axes[j].hide()
        
        plt.tight_layout()
        plt.savefig('wisdom_distributions.png', dpi=300, bbox_inches='tight')
        print(f"\nScore distributions saved as 'wisdom_distributions.png'")
        
        # Box plots for comparison
        if len(available_scores) > 1:
            plt.figure(figsize=(12, 6))
            score_data = self.df[available_scores].melt(var_name='Scale', value_name='Score')
            sns.boxplot(data=score_data, x='Scale', y='Score')
            plt.xticks(rotation=45)
            plt.title('WISDOM Subscale Score Distributions')
            plt.tight_layout()
            plt.savefig('wisdom_boxplots.png', dpi=300, bbox_inches='tight')
            print(f"Boxplot comparison saved as 'wisdom_boxplots.png'")
    
    def export_report(self, filename=None):
        """Export comprehensive analysis report"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'wisdom_analysis_report_{timestamp}.txt'
        
        with open(filename, 'w') as f:
            f.write("WISDOM QUESTIONNAIRE ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data file: {self.data_file}\n")
            f.write(f"Sample size: {len(self.df) if self.df is not None else 0}\n\n")
            
            if 'basic_stats' in self.results:
                f.write("DESCRIPTIVE STATISTICS:\n")
                f.write("-" * 30 + "\n")
                for scale, stats in self.results['basic_stats'].items():
                    f.write(f"\n{scale.replace('_', ' ').title()}:\n")
                    for stat, value in stats.items():
                        f.write(f"  {stat}: {value:.2f}\n")
            
            if 'reliability' in self.results:
                f.write(f"\nRELIABILITY (Cronbach's α):\n")
                f.write("-" * 30 + "\n")
                for scale, alpha in self.results['reliability'].items():
                    f.write(f"{scale.replace('_', ' ').title()}: {alpha:.3f}\n")
            
            f.write(f"\nFiles generated:\n")
            f.write("- wisdom_correlations.png (correlation heatmap)\n")
            f.write("- wisdom_distributions.png (score distributions)\n")
            f.write("- wisdom_boxplots.png (comparison boxplots)\n")
        
        print(f"\nComprehensive report saved as '{filename}'")
    
    def run_complete_analysis(self):
        """Run all analyses and generate reports"""
        print("WISDOM QUESTIONNAIRE DATA ANALYSIS")
        print("=" * 50)
        
        # Try to load CSV first, then JSON files
        if not self.load_data():
            if not self.load_json_data():
                print("No data found to analyze.")
                return False
        
        # Run analyses
        self.basic_statistics()
        self.correlation_analysis()
        self.reliability_analysis()
        self.generate_plots()
        self.export_report()
        
        print("\n" + "=" * 50)
        print("Analysis complete! Check the generated files.")
        print("=" * 50)
        
        return True

def main():
    """Main function to run the analysis"""
    analyzer = WisdomAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    # Install required packages if needed
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import scipy.stats
    except ImportError:
        print("Required packages not found. Install with:")
        print("pip install pandas matplotlib seaborn scipy")
        exit(1)
    
    main()
