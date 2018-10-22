num_aggregations = {
        'AMT_ANNUITY': [('max', np.nanmax), ('mean', np.nanmean), ('sum', np.nansum), ('std', np.nanstd),
        ('log_mean', lambda x: np.nanmean(np.log1p(x))),
                           ('log_std', lambda x: np.nanstd(np.log1p(x))), ('median', np.nanmedian),
                       ('log_sum', lambda x: np.nansum(np.log1p(x)))],
        'AMT_APPLICATION': ['min', 'max', 'mean'],
        'AMT_CREDIT': [('max', np.nanmax), ('mean', np.nanmean), ('sum', np.nansum), ('std', np.nanstd),
        ('log_mean', lambda x: np.nanmean(np.log1p(x))),('median', np.nanmedian),
                           ('log_std', lambda x: np.nanstd(np.log1p(x))), 
                       ('log_sum', lambda x: np.nansum(np.log1p(x)))],
        'APP_CREDIT_PERC': ['min', 'max', 'mean', 'var', 'median'],
        'AMT_DOWN_PAYMENT': [('max', np.nanmax), ('mean', np.nanmean), ('median', np.nanmedian),
                             ('sum', np.nansum), ('std', np.nanstd),
        ('log_mean', lambda x: np.nanmean(np.log1p(x))), 
                       ('log_sum', lambda x: np.nansum(np.log1p(x)))],
        'AMT_GOODS_PRICE': [('max', np.nanmax), ('mean', np.nanmean), ('sum', np.nansum), ('std', np.nanstd),
        ('log_mean', lambda x: np.nanmean(np.log1p(x))), ('median', np.nanmedian),
                       ('log_sum', lambda x: np.nansum(np.log1p(x)))],
        'HOUR_APPR_PROCESS_START': ['min', 'max', 'mean'],
        'RATE_DOWN_PAYMENT': ['min', 'max', 'mean'],
        'DAYS_DECISION': ['min', 'max', 'mean', 'median'],
        'CNT_PAYMENT': ['mean', 'sum', 'median'],
        'DIF_ASK_GOOD':['mean','median'],
    }
    # Previous applications categorical features
    cat_aggregations = {}
    for cat in cat_cols:
        cat_aggregations[cat] = ['mean']
    
    prev_agg = prev.groupby('SK_ID_CURR').agg({**num_aggregations, **cat_aggregations})
    
    
    
def one_hot_encoder(df, nan_as_category = True):
    original_columns = list(df.columns)
    categorical_columns = [col for col in df.columns if df[col].dtype == 'object']
    df = pd.get_dummies(df, columns= categorical_columns, dummy_na= nan_as_category)
    new_columns = [c for c in df.columns if c not in original_columns]
    return df, new_columns
