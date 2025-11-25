import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import entropy, skew, kurtosis
from sklearn.preprocessing import LabelEncoder
import json

class ComprehensiveStatisticalSummary:
    def __init__(self, df):
        self.df = df
        self.summary = {}
        
    def generate_complete_summary(self):
        """Generate all statistical summaries needed for synthetic data"""
        
        self.summary = {
            'dataset_metadata': self._dataset_metadata(),
            'numerical_features': self._numerical_statistics(),
            'categorical_features': self._categorical_statistics(),
            'datetime_features': self._datetime_statistics(),
            'text_features': self._text_statistics(),
            'relationships': self._relationship_statistics(),
            'distributions': self._distribution_analysis(),
            'constraints': self._constraint_analysis(),
            'patterns': self._pattern_analysis(),
            'anomaly_characteristics': self._anomaly_characteristics()
        }
        
        return self.summary
    
    def _dataset_metadata(self):
        """Basic dataset information"""
        return {
            'num_records': len(self.df),
            'num_features': len(self.df.columns),
            'missing_data_percentage': (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100,
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'duplicate_rows': self.df.duplicated().sum(),
            'feature_types': {
                'numerical': len(self.df.select_dtypes(include=[np.number]).columns),
                'categorical': len(self.df.select_dtypes(include=['object', 'category']).columns),
                'datetime': len(self.df.select_dtypes(include=['datetime64']).columns)
            }
        }
    
    def _numerical_statistics(self):
        """Comprehensive numerical feature statistics"""
        numerical_stats = {}
        
        for col in self.df.select_dtypes(include=[np.number]).columns:
            data = self.df[col].dropna()
            
            numerical_stats[col] = {
                # Central tendency
                'mean': float(data.mean()),
                'median': float(data.median()),
                'mode': float(data.mode()[0]) if len(data.mode()) > 0 else None,
                'trimmed_mean_10': float(stats.trim_mean(data, 0.1)),
                'geometric_mean': float(stats.gmean(data[data > 0])) if (data > 0).any() else None,
                'harmonic_mean': float(stats.hmean(data[data > 0])) if (data > 0).any() else None,
                
                # Dispersion
                'std': float(data.std()),
                'variance': float(data.var()),
                'range': float(data.max() - data.min()),
                'iqr': float(data.quantile(0.75) - data.quantile(0.25)),
                'mad': float(np.median(np.abs(data - data.median()))),  # Median Absolute Deviation
                'coefficient_of_variation': float(data.std() / data.mean()) if data.mean() != 0 else None,
                
                # Extremes
                'min': float(data.min()),
                'max': float(data.max()),
                
                # Percentiles (detailed)
                'percentiles': {
                    'p1': float(data.quantile(0.01)),
                    'p5': float(data.quantile(0.05)),
                    'p10': float(data.quantile(0.10)),
                    'p25': float(data.quantile(0.25)),
                    'p50': float(data.quantile(0.50)),
                    'p75': float(data.quantile(0.75)),
                    'p90': float(data.quantile(0.90)),
                    'p95': float(data.quantile(0.95)),
                    'p99': float(data.quantile(0.99))
                },
                
                # Shape
                'skewness': float(data.skew()),
                'kurtosis': float(data.kurtosis()),
                'is_symmetric': abs(data.skew()) < 0.5,
                
                # Distribution characteristics
                'is_unimodal': self._check_unimodality(data),
                'num_modes': len(self._find_modes(data)),
                
                # Missing data
                'missing_count': int(self.df[col].isnull().sum()),
                'missing_percentage': float((self.df[col].isnull().sum() / len(self.df)) * 100),
                
                # Outliers
                'outlier_count_iqr': int(self._count_outliers_iqr(data)),
                'outlier_count_zscore': int(self._count_outliers_zscore(data)),
                'outlier_percentage': float((self._count_outliers_iqr(data) / len(data)) * 100),
                
                # Uniqueness
                'unique_count': int(data.nunique()),
                'unique_percentage': float((data.nunique() / len(data)) * 100),
                'is_constant': data.nunique() == 1,
                
                # Zero/Negative analysis
                'zero_count': int((data == 0).sum()),
                'negative_count': int((data < 0).sum()),
                'positive_count': int((data > 0).sum()),
                
                # Statistical tests
                'normality_test': {
                    'statistic': float(stats.normaltest(data)[0]) if len(data) >= 8 else None,
                    'p_value': float(stats.normaltest(data)[1]) if len(data) >= 8 else None,
                    'is_normal': bool(stats.normaltest(data)[1] > 0.05) if len(data) >= 8 else None
                }
            }
        
        return numerical_stats
    
    def _categorical_statistics(self):
        """Comprehensive categorical feature statistics"""
        categorical_stats = {}
        
        for col in self.df.select_dtypes(include=['object', 'category']).columns:
            data = self.df[col].dropna()
            value_counts = data.value_counts()
            value_proportions = data.value_counts(normalize=True)
            
            categorical_stats[col] = {
                # Cardinality
                'unique_count': int(data.nunique()),
                'unique_percentage': float((data.nunique() / len(data)) * 100),
                
                # Distribution
                'value_counts': value_counts.head(50).to_dict(),  # Top 50 values
                'value_proportions': value_proportions.head(50).to_dict(),
                
                # Concentration metrics
                'entropy': float(entropy(value_counts)),
                'gini_coefficient': float(self._gini_coefficient(value_counts)),
                'concentration_ratio_top5': float(value_proportions.head(5).sum()),
                'concentration_ratio_top10': float(value_proportions.head(10).sum()),
                
                # Most/Least common
                'most_common': {
                    'value': str(value_counts.index[0]),
                    'count': int(value_counts.iloc[0]),
                    'percentage': float(value_proportions.iloc[0] * 100)
                },
                'least_common': {
                    'value': str(value_counts.index[-1]),
                    'count': int(value_counts.iloc[-1]),
                    'percentage': float(value_proportions.iloc[-1] * 100)
                },
                
                # Frequency bins
                'frequency_distribution': {
                    'singleton_count': int((value_counts == 1).sum()),  # Values appearing once
                    'rare_count': int((value_counts <= 5).sum()),  # Values appearing ≤5 times
                    'common_count': int((value_counts > 100).sum())  # Values appearing >100 times
                },
                
                # Missing data
                'missing_count': int(self.df[col].isnull().sum()),
                'missing_percentage': float((self.df[col].isnull().sum() / len(self.df)) * 100),
                
                # String characteristics (if applicable)
                'avg_length': float(data.astype(str).str.len().mean()) if data.dtype == 'object' else None,
                'min_length': int(data.astype(str).str.len().min()) if data.dtype == 'object' else None,
                'max_length': int(data.astype(str).str.len().max()) if data.dtype == 'object' else None,
                
                # Pattern detection
                'contains_numbers': bool(data.astype(str).str.contains(r'\d').any()) if data.dtype == 'object' else None,
                'contains_special_chars': bool(data.astype(str).str.contains(r'[^a-zA-Z0-9\s]').any()) if data.dtype == 'object' else None,
                
                # Case analysis (for string data)
                'all_uppercase_percentage': float((data.astype(str).str.isupper().sum() / len(data)) * 100) if data.dtype == 'object' else None,
                'all_lowercase_percentage': float((data.astype(str).str.islower().sum() / len(data)) * 100) if data.dtype == 'object' else None
            }
        
        return categorical_stats
    
    def _datetime_statistics(self):
        """Comprehensive datetime feature statistics"""
        datetime_stats = {}
        
        for col in self.df.select_dtypes(include=['datetime64']).columns:
            data = self.df[col].dropna()
            
            datetime_stats[col] = {
                # Range
                'min_date': str(data.min()),
                'max_date': str(data.max()),
                'range_days': int((data.max() - data.min()).days),
                
                # Central tendency
                'median_date': str(data.median()),
                'mode_date': str(data.mode()[0]) if len(data.mode()) > 0 else None,
                
                # Granularity
                'unique_dates': int(data.dt.date.nunique()),
                'unique_hours': int(data.dt.hour.nunique()) if data.dt.hour.nunique() > 1 else None,
                'unique_minutes': int(data.dt.minute.nunique()) if data.dt.minute.nunique() > 1 else None,
                
                # Temporal patterns
                'day_of_week_distribution': data.dt.dayofweek.value_counts().to_dict(),
                'month_distribution': data.dt.month.value_counts().to_dict(),
                'hour_distribution': data.dt.hour.value_counts().to_dict() if data.dt.hour.nunique() > 1 else None,
                'quarter_distribution': data.dt.quarter.value_counts().to_dict(),
                
                # Time gaps
                'avg_gap_days': float(data.diff().dt.days.mean()) if len(data) > 1 else None,
                'median_gap_days': float(data.diff().dt.days.median()) if len(data) > 1 else None,
                'max_gap_days': float(data.diff().dt.days.max()) if len(data) > 1 else None,
                
                # Business day analysis
                'weekday_percentage': float((data.dt.dayofweek < 5).sum() / len(data) * 100),
                'weekend_percentage': float((data.dt.dayofweek >= 5).sum() / len(data) * 100),
                
                # Missing data
                'missing_count': int(self.df[col].isnull().sum()),
                'missing_percentage': float((self.df[col].isnull().sum() / len(self.df)) * 100)
            }
        
        return datetime_stats
    
    def _text_statistics(self):
        """Statistics for text/string columns (different from categorical)"""
        text_stats = {}
        
        text_columns = []
        for col in self.df.select_dtypes(include=['object']).columns:
            # Consider it text if avg length > 50 or high cardinality
            if self.df[col].astype(str).str.len().mean() > 50 or self.df[col].nunique() / len(self.df) > 0.5:
                text_columns.append(col)
        
        for col in text_columns:
            data = self.df[col].dropna().astype(str)
            
            text_stats[col] = {
                # Length statistics
                'avg_length': float(data.str.len().mean()),
                'median_length': float(data.str.len().median()),
                'min_length': int(data.str.len().min()),
                'max_length': int(data.str.len().max()),
                'std_length': float(data.str.len().std()),
                
                # Word statistics
                'avg_word_count': float(data.str.split().str.len().mean()),
                'median_word_count': float(data.str.split().str.len().median()),
                
                # Character composition
                'avg_uppercase_percentage': float((data.str.count(r'[A-Z]') / data.str.len()).mean() * 100),
                'avg_digit_percentage': float((data.str.count(r'\d') / data.str.len()).mean() * 100),
                'avg_special_char_percentage': float((data.str.count(r'[^a-zA-Z0-9\s]') / data.str.len()).mean() * 100),
                
                # Common patterns
                'contains_email_pattern': bool(data.str.contains(r'[\w\.-]+@[\w\.-]+').any()),
                'contains_url_pattern': bool(data.str.contains(r'http[s]?://').any()),
                'contains_phone_pattern': bool(data.str.contains(r'\d{3}[-.]?\d{3}[-.]?\d{4}').any()),
                
                # Vocabulary
                'unique_words': int(len(set(' '.join(data).split()))),
                'lexical_diversity': float(len(set(' '.join(data).split())) / len(' '.join(data).split()))
            }
        
        return text_stats
    
    def _relationship_statistics(self):
        """Feature relationships and dependencies"""
        relationships = {
            'correlations': {},
            'associations': {},
            'dependencies': {},
            'multicollinearity': {}
        }
        
        # Numerical correlations
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            
            # Pearson correlations
            relationships['correlations']['pearson'] = {}
            for i, col1 in enumerate(corr_matrix.columns):
                for col2 in corr_matrix.columns[i+1:]:
                    corr_val = float(corr_matrix.loc[col1, col2])
                    if abs(corr_val) > 0.1:  # Only store significant correlations
                        relationships['correlations']['pearson'][f"{col1}___{col2}"] = corr_val
            
            # Spearman correlations (rank-based, captures non-linear)
            spearman_matrix = numeric_df.corr(method='spearman')
            relationships['correlations']['spearman'] = {}
            for i, col1 in enumerate(spearman_matrix.columns):
                for col2 in spearman_matrix.columns[i+1:]:
                    corr_val = float(spearman_matrix.loc[col1, col2])
                    if abs(corr_val) > 0.1:
                        relationships['correlations']['spearman'][f"{col1}___{col2}"] = corr_val
            
            # Variance Inflation Factor (VIF) for multicollinearity
            from statsmodels.stats.outliers_influence import variance_inflation_factor
            
            try:
                vif_data = numeric_df.dropna()
                if len(vif_data) > len(vif_data.columns):
                    relationships['multicollinearity'] = {
                        col: float(variance_inflation_factor(vif_data.values, i))
                        for i, col in enumerate(vif_data.columns)
                    }
            except:
                pass
        
        # Categorical associations (Cramér's V)
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 1:
            relationships['associations']['cramers_v'] = {}
            for i, col1 in enumerate(categorical_cols):
                for col2 in categorical_cols[i+1:]:
                    cramers = self._cramers_v(self.df[col1], self.df[col2])
                    if cramers > 0.1:
                        relationships['associations']['cramers_v'][f"{col1}___{col2}"] = float(cramers)
        
        # Mixed correlations (numerical-categorical)
        relationships['mixed_relationships'] = {}
        for num_col in numeric_df.columns:
            for cat_col in categorical_cols:
                # ANOVA F-statistic
                groups = [group[num_col].dropna() for name, group in self.df.groupby(cat_col)]
                if len(groups) > 1 and all(len(g) > 0 for g in groups):
                    f_stat, p_val = stats.f_oneway(*groups)
                    if p_val < 0.05:  # Significant relationship
                        relationships['mixed_relationships'][f"{num_col}___{cat_col}"] = {
                            'f_statistic': float(f_stat),
                            'p_value': float(p_val),
                            'eta_squared': float(self._eta_squared(self.df, num_col, cat_col))
                        }
        
        # Mutual information (captures non-linear dependencies)
        from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
        
        relationships['mutual_information'] = {}
        if len(numeric_df.columns) > 1:
            for target_col in numeric_df.columns:
                features = numeric_df.drop(columns=[target_col]).fillna(0)
                if len(features.columns) > 0:
                    mi_scores = mutual_info_regression(features, numeric_df[target_col].fillna(0))
                    relationships['mutual_information'][target_col] = {
                        features.columns[i]: float(score)
                        for i, score in enumerate(mi_scores)
                        if score > 0.01
                    }
        
        return relationships
    
    def _distribution_analysis(self):
        """Detailed distribution fitting and analysis"""
        distributions = {}
        
        for col in self.df.select_dtypes(include=[np.number]).columns:
            data = self.df[col].dropna()
            
            distributions[col] = {
                'best_fit_distribution': self._fit_distribution(data),
                'distribution_parameters': {},
                'goodness_of_fit': {}
            }
            
            # Test common distributions
            dist_tests = {
                'normal': stats.norm,
                'lognormal': stats.lognorm,
                'exponential': stats.expon,
                'gamma': stats.gamma,
                'beta': stats.beta,
                'uniform': stats.uniform,
                'weibull': stats.weibull_min
            }
            
            for dist_name, dist_func in dist_tests.items():
                try:
                    params = dist_func.fit(data)
                    ks_stat, p_value = stats.kstest(data, dist_name, args=params)
                    
                    distributions[col]['distribution_parameters'][dist_name] = {
                        'params': [float(p) for p in params],
                        'ks_statistic': float(ks_stat),
                        'p_value': float(p_value),
                        'is_good_fit': bool(p_value > 0.05)
                    }
                except:
                    pass
        
        return distributions
    
    def _constraint_analysis(self):
        """Detect data constraints and business rules"""
        constraints = {
            'range_constraints': {},
            'logical_constraints': [],
            'uniqueness_constraints': [],
            'functional_dependencies': []
        }
        
        # Range constraints for numerical columns
        for col in self.df.select_dtypes(include=[np.number]).columns:
            data = self.df[col].dropna()
            constraints['range_constraints'][col] = {
                'min': float(data.min()),
                'max': float(data.max()),
                'always_positive': bool((data >= 0).all()),
                'always_negative': bool((data <= 0).all()),
                'always_integer': bool((data == data.astype(int)).all()),
                'bounded_0_1': bool((data >= 0).all() and (data <= 1).all())
            }
        
        # Uniqueness constraints
        for col in self.df.columns:
            if self.df[col].nunique() == len(self.df):
                constraints['uniqueness_constraints'].append(col)
        
        # Detect functional dependencies (if A determines B)
        for col1 in self.df.columns:
            for col2 in self.df.columns:
                if col1 != col2:
                    grouped = self.df.groupby(col1)[col2].nunique()
                    if (grouped == 1).all():
                        constraints['functional_dependencies'].append({
                            'determinant': col1,
                            'dependent': col2
                        })
        
        # Sum constraints (e.g., percentages that sum to 100)
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            row_sums = self.df[numeric_cols].sum(axis=1)
            if row_sums.std() < 0.01:  # Nearly constant sum
                constraints['logical_constraints'].append({
                    'type': 'sum_constraint',
                    'columns': list(numeric_cols),
                    'target_sum': float(row_sums.mean())
                })
        
        return constraints
    
    def _pattern_analysis(self):
        """Detect temporal, sequential, and other patterns"""
        patterns = {
            'temporal_patterns': {},
            'sequential_patterns': {},
            'cyclic_patterns': {}
        }
        
        # Temporal patterns (if datetime column exists)
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(datetime_cols) > 0:
            for dt_col in datetime_cols:
                sorted_df = self.df.sort_values(dt_col)
                
                # Trend detection in numerical columns
                for num_col in self.df.select_dtypes(include=[np.number]).columns:
                    data = sorted_df[[dt_col, num_col]].dropna()
                    if len(data) > 10:
                        # Linear trend
                        x = np.arange(len(data))
                        y = data[num_col].values
                        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                        
                        patterns['temporal_patterns'][f"{dt_col}_{num_col}"] = {
                            'trend_slope': float(slope),
                            'trend_strength': float(r_value**2),
                            'trend_significant': bool(p_value < 0.05)
                        }
                
                # Seasonality detection
                if dt_col in datetime_cols:
                    for num_col in self.df.select_dtypes(include=[np.number]).columns:
                        monthly_avg = self.df.groupby(self.df[dt_col].dt.month)[num_col].mean()
                        if len(monthly_avg) >= 12:
                            patterns['cyclic_patterns'][f"{dt_col}_{num_col}"] = {
                                'monthly_pattern': monthly_avg.to_dict(),
                                'seasonality_strength': float(monthly_avg.std() / monthly_avg.mean())
                            }
        
        # Sequential patterns (autocorrelation)
        for col in self.df.select_dtypes(include=[np.number]).columns:
            data = self.df[col].dropna()
            if len(data) > 10:
                # Lag-1 autocorrelation
                autocorr = data.autocorr(lag=1)
                if not np.isnan(autocorr):
                    patterns['sequential_patterns'][col] = {
                        'lag1_autocorrelation': float(autocorr),
                        'is_autocorrelated': bool(abs(autocorr) > 0.3)
                    }
        
        return patterns
    
    def _anomaly_characteristics(self):
        """Characteristics of anomalies/outliers for replication"""
        anomalies = {}
        
        for col in self.df.select_dtypes(include=[np.number]).columns:
            data = self.df[col].dropna()
            
            # IQR method
            q1, q3 = data.quantile([0.25, 0.75])
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = data[(data < lower_bound) | (data > upper_bound)]
            
            if len(outliers) > 0:
                anomalies[col] = {
                    'outlier_percentage': float(len(outliers) / len(data) * 100),
                    'outlier_distribution': {
                        'below_lower_bound': int((data < lower_bound).sum()),
                        'above_upper_bound': int((data > upper_bound).sum())
                    },
                    'extreme_values': {
                        'lowest': float(data.nsmallest(5).mean()),
                        'highest': float(data.nlargest(5).mean())
                    }
                }
        
        return anomalies
    
    # Helper methods
    def _count_outliers_iqr(self, data):
        q1, q3 = data.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return ((data < lower) | (data > upper)).sum()
    
    def _count_outliers_zscore(self, data):
        z_scores = np.abs(stats.zscore(data))
        return (z_scores > 3).sum()
    
    def _check_unimodality(self, data):
        # Simple check using kernel density estimation
        from scipy.signal import find_peaks
        hist, bins = np.histogram(data, bins=30)
        peaks, _ = find_peaks(hist)
        return len(peaks) == 1
    
    def _find_modes(self, data):
        from scipy.signal import find_peaks
        hist, bins = np.histogram(data, bins=30)
        peaks, _ = find_peaks(hist)
        return peaks
    
    def _gini_coefficient(self, value_counts):
        """Calculate Gini coefficient for concentration"""
        sorted_values = np.sort(value_counts.values)
        n = len(sorted_values)
        cumsum = np.cumsum(sorted_values)
        return (2 * np.sum((np.arange(1, n+1)) * sorted_values)) / (n * cumsum[-1]) - (n + 1) / n
    
    def _cramers_v(self, x, y):
        """Cramér's V for categorical association"""
        confusion_matrix = pd.crosstab(x, y)
        chi2 = stats.chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        min_dim = min(confusion_matrix.shape) - 1
        return np.sqrt(chi2 / (n * min_dim))
    
    def _eta_squared(self, df, numeric_col, categorical_col):
        """Effect size for ANOVA"""
        groups = [group[numeric_col].dropna() for name, group in df.groupby(categorical_col)]
        grand_mean = df[numeric_col].mean()
        ss_between = sum(len(group) * (group.mean() - grand_mean)**2 for group in groups)
        ss_total = sum((df[numeric_col] - grand_mean)**2)
        return ss_between / ss_total if ss_total != 0 else 0
    
    def _fit_distribution(self, data):
        """Find best fitting distribution"""
        distributions = [stats.norm, stats.lognorm, stats.expon, stats.gamma]
        best_dist = None
        best_p = 0
        
        for dist in distributions:
            try:
                params = dist.fit(data)
                ks_stat, p_value = stats.kstest(data, dist.name, args=params)
                if p_value > best_p:
                    best_p = p_value
                    best_dist = dist.name
            except:
                continue
        
        return best_dist if best_dist else 'unknown'
    
    def save_to_json(self, filepath):
        """Save summary to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.summary, f, indent=2)
    
    def get_llm_prompt(self):
        """Generate a prompt for LLM to create synthetic data"""
        prompt = f"""Generate synthetic data matching these comprehensive statistical properties:

{json.dumps(self.summary, indent=2)}

Requirements:
1. Match all central tendency measures (mean, median, mode)
2. Preserve dispersion characteristics (std, variance, IQR)
3. Maintain distribution shapes (skewness, kurtosis)
4. Respect all correlations and relationships between features
5. Honor all constraints (range, uniqueness, functional dependencies)
6. Replicate temporal and sequential patterns
7. Include appropriate outliers matching the anomaly characteristics
8. Maintain categorical value distributions and frequencies
9. Preserve missing data patterns
10. Follow all detected business rules and logical constraints

Output format: CSV with {self.summary['dataset_metadata']['num_records']} rows"""
        
        return prompt

# Usage example
if __name__ == "__main__":
    # Example with sample data
    df = pd.DataFrame({
        'age': np.random.normal(40, 15, 1000),
        'salary': np.random.lognormal(11, 0.5, 1000),
        'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR'], 1000),
        'join_date': pd.date_range('2015-01-01', periods=1000, freq='D'),
        'performance_score': np.random.beta(8, 2, 1000)
    })
    
    # Generate comprehensive summary
    summarizer = ComprehensiveStatisticalSummary(df)
    complete_summary = summarizer.generate_complete_summary()
    
    # Save to file
    summarizer.save_to_json('comprehensive_summary.json')
    
    # Get LLM prompt
    llm_prompt = summarizer.get_llm_prompt()
    print(llm_prompt)
