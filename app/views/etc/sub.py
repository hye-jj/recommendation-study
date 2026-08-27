import pandas as pd
import numpy as np
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity

def data_read(num, cus, rating):
    cus_id = int(num)
    id_fre_cluster = cus[cus.cno == cus_id].fre_clu.values[0]
    id_age_cluster = cus[cus.cno == cus_id].age_clu.values[0]
    fre_data = cus[cus.age_clu == id_fre_cluster]
    age_data = cus[cus.age_clu == id_age_cluster]  # .cno.values
    fre_X = fre_data[['cno']].merge(rating, on='cno', how='inner') 
    age_X = age_data[['cno']].merge(rating, on='cno', how='inner')
    return fre_X, age_X


def cal_similarity(df):
    # User CF - row : 사용자 , column : 아이템, values : 평가점수
    # Item CF - row : 아이템 , column : 사용자, values : 평가점수
    piv = df.pivot_table(index=['cno'], columns=['scls_c_nm'], values='user_rating')
    piv_norm = piv.apply(lambda x: (x-np.mean(x))/(np.max(x)-np.min(x)), axis=1) # min-max scaling 
    piv_norm.fillna(0, inplace=True)
    piv_norm = piv_norm.T
    piv_norm = piv_norm.loc[:, (piv_norm != 0).any(axis=0)]
    piv_sparse = sp.sparse.csr_matrix(piv_norm.values)
    item_similarity = cosine_similarity(piv_sparse)
    user_similarity = cosine_similarity(piv_sparse.T)  # 전치
    item_sim_df = pd.DataFrame(item_similarity, index = piv_norm.index, columns = piv_norm.index)
    user_sim_df = pd.DataFrame(user_similarity, index = piv_norm.columns, columns = piv_norm.columns)
    
    return item_sim_df, user_sim_df


# 유사 상품 추천
def top_item(item_nm, item_sim_df):
    li = []
    count = 1
    print('Similar shows to {} include: '.format(item_nm))
    result = item_sim_df.loc[~item_sim_df.index.isin([item_nm]), item_nm].sort_values(ascending = False)[:10]
    for item, score in result.items():
        li.append('No. {}: {}  ({:.2f})'.format(count, item , score))
        count +=1 
    return li


# 유사 유저
def top_users(user, fre_X, user_sim_df):
    li = []
    if user not in fre_X.cno.values:
        li.append('No data available on user {}'.format(user))

    print('Most Similar Users:\n', user)
    result = user_sim_df.sort_values(by=user, ascending=False).loc[:,user][1:11]
    for user, sim in result.items():
        li.append('User #{0}, Similarity value: {1:.2f}'.format(user, sim))
        
    return li


