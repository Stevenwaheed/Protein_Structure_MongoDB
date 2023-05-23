import streamlit as st
import pandas as pd
from pymongo import MongoClient
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pymongo

client = MongoClient('mongodb+srv://eslam:heartizm@cluster0.qhy7hob.mongodb.net/?retryWrites=true&w=majority')
db = client.get_database('Protein_Structure')


Embbeded=[]

def data_upload(collection_name):
    
    client = MongoClient('mongodb+srv://eslam:heartizm@cluster0.qhy7hob.mongodb.net/?retryWrites=true&w=majority')
    db = client.get_database('Protein_Structure')
    
    collection = db.get_collection(collection_name)
    
    lst = []
    for record in collection.find():
        lst.append(record)
    
    df = pd.DataFrame(lst)
    return df


def delete_record(record, collection):
    collection = db.get_collection(collection)
    
    print(record)
    record_data = pd.DataFrame([record])

    record_data.dropna(axis=1, inplace=True)

    final_data = {}
    count = 0
    for col in record_data.columns:
        final_data[col] = record_data.values[0][count]
        count+=1
        
    result = collection.delete_one(final_data)
    
    st.error('Deleted Successfully')
    print(result.deleted_count, ' document deleted')

    
def update_record(collection, user_choice):
    df = data_upload(collection)
    try:
        record = show(df)
        
        collection = db.get_collection(collection)
        
        
        print(record)
        print('-------------------------------------------')
        province = col1.text_input(user_choice, record[user_choice])
        
        del record[user_choice]
        
        if st.button('Update'):
            st.success('Updated Successfully')
            result = collection.update_one(record, {'$set': {user_choice:province}})
            print(result.modified_count)
    except:
        pass


def show(df):
    data = df.iloc[:, 1:]
    new_data = data.replace('-', None)
    
    gd = GridOptionsBuilder.from_dataframe(new_data)
    gd.configure_selection(selection_mode='single', use_checkbox=True)
    grid_options = gd.build()

    grid_table = AgGrid(new_data.iloc[:2000, :], gridOptions=grid_options, height=500)
    
    values = list(grid_table['selected_rows'][0].values())[1:]
    keys = list(grid_table['selected_rows'][0].keys())[1:]
    
    record = {}
    for key, value in zip(keys, values):
        record[key] = value
    
    return record
        

def seq_columns():
    query = {}
    col1, col2, col3, col4  = st.columns(4)
    # structureId,chainId,sequence,residueCount,macromoleculeType
    structureId_field = col1.checkbox(label='structureId')
    structureId_field_text = col2.text_input(label='structureId')
    
    chainId_field = col1.checkbox(label='chainId')
    chainId_field_text = col3.text_input(label='chainId')
    
    
    sequence_field = col1.checkbox(label='sequence')
    sequence_field_text = col2.text_input(label='sequence')
    
    residueCount_field = col1.checkbox(label='residueCount')
    residueCount_field_text = col4.text_input(label='residueCount')
    
    # macromoleculeType_field = col1.checkbox(label='macromoleculeType')
    # macromoleculeType_field_text = col2.text_input(label='macromoleculeType')
    
    
    if structureId_field:
        query['structureId'] = structureId_field_text
        
    if chainId_field:
        query['chainId'] = chainId_field_text
    
    if sequence_field:
        query['sequence'] = sequence_field_text
    
    # if macromoleculeType_field:
    #     query['macromoleculeType'] = macromoleculeType_field_text
    
    if residueCount_field:
        query['residueCount'] = int(residueCount_field_text)

    return query


def columns():
    query={}
    col1, col2, col3, col4  = st.columns(4)
    structureId_field = col1.checkbox(label='structureId')
    structureId_field_text = col2.text_input(label='structureId')
    
    classification_field = col1.checkbox(label='classification')
    classification_field_text = col3.text_input(label='classification')
    
    
    macromoleculeType_field = col1.checkbox(label='macromoleculeType')
    macromoleculeType_field_text = col3.text_input(label='macromoleculeType')
    
    
    residueCount_field = col1.checkbox(label='residueCount')
    residueCount_field_text = col2.text_input(label='residueCount')
    
    resolution_field = col1.checkbox(label='resolution')
    resolution_field_text = col2.text_input(label='resolution')
    
    structureMolecularWeight_field = col1.checkbox(label='MolecularWeight')
    structureMolecularWeight_field_text = col2.text_input(label='MolecularWeight')
    
    phValue_field = col1.checkbox(label='phValue')
    phValue_field_text = col4.slider(label='phValue', min_value=1, max_value=14)
    
    publicationYear_field = col1.checkbox(label='publicationYear')
    publicationYear_field_text = col4.slider(label='publicationYear', value=[1900, 2500])
    # print(publicationYear_field_text)
    
    densityMatthews_field = col1.checkbox(label='densityMatthews')
    densityMatthews_field_text = col4.slider(label='densityMatthews', value=[0.0, 100.0])
    
    densityPercentSol_field = col1.checkbox(label='densityPercentSol')
    densityPercentSol_field_text = col4.slider(label='densityPercentSol', value=[0.0, 100.0])
    
    pdbxDetails_field = col1.checkbox(label='pdbxDetails')
    pdbxDetails_field_text = col2.text_input(label='pdbxDetails')
    
    crystallizationMethod_field = col1.checkbox(label='crystallizationMethod')
    crystallizationMethod_field_text = col3.text_input(label='crystallizationMethod')
    
    crystallizationTempK_field = col1.checkbox(label='crystallizationTempK')
    crystallizationTempK_field_text = col3.text_input(label='crystallizationTempK')
    
    experimentalTechnique_field = col1.checkbox(label='experimentalTechnique')
    experimentalTechnique_field_text = col3.text_input(label='experimentalTechnique')
    
    
    
    if structureId_field:
        query['structureId'] = structureId_field_text
        
    if classification_field:
        query['classification'] = classification_field_text
    
    if experimentalTechnique_field:
        query['experimentalTechnique'] = experimentalTechnique_field_text
    
    if macromoleculeType_field:
        query['macromoleculeType'] = macromoleculeType_field_text
    
    if resolution_field:
        query['resolution'] = resolution_field_text
    
    if publicationYear_field:
        query['publicationYear'] = publicationYear_field_text
    
    if residueCount_field:
        query['residueCount'] = int(residueCount_field_text)
    
    if structureMolecularWeight_field:
        query['structureMolecularWeight'] = structureMolecularWeight_field_text
        
    if crystallizationMethod_field:
        query['crystallizationMethod'] = crystallizationMethod_field_text
        
    if crystallizationTempK_field:
        query['crystallizationTempK'] = crystallizationTempK_field_text
        
    if densityMatthews_field:
        query['densityMatthews'] = {'$gte': densityMatthews_field_text[0], '$lte': densityMatthews_field_text[1]}
    
    if densityPercentSol_field:
        query['densityPercentSol'] = {'$gte': densityPercentSol_field_text[0], '$lte': densityPercentSol_field_text[1]}
    
    if pdbxDetails_field:
        query['pdbxDetails'] = pdbxDetails_field_text
    
    if phValue_field:
        query['phValue'] = phValue_field_text
        
    return query


def map_reduce(operation_choice, user_choice, column_choice, collection):
    if operation_choice=='avg':
        # Pipeline for aggregation
        pipeline = [
            {"$group": {
                "_id": "$"+user_choice,
                "count": {"$sum": 1},
                "total": {"$sum": "$"+column_choice}
            }},
            {"$project": {
                user_choice: "$_id",
                "count": 1,
                "average": {"$divide": ["$total", "$count"]}
            }},
            {"$sort": {user_choice: 1}}
        ]

        # Execute aggregation
        result = collection.aggregate(pipeline)

        lst = []
        for doc in result:
            lst.append(doc)
            
        df = pd.DataFrame(lst)
        st.dataframe(df.astype('str'), width=700)
    
    
    
    if operation_choice=='max' or operation_choice=='min':
        pipeline = [
            {"$group": {
                "_id": "$"+user_choice,
                "Max": {"$"+operation_choice: "$"+column_choice}
            }}
        ]

        result = collection.aggregate(pipeline)
        
        lst = []
        for doc in result:
            lst.append(doc)
            
        df = pd.DataFrame(lst)
        st.dataframe(df.astype('str'))


def indexeing(user_choice, order_choice):
    if order_choice=='Ascending':
        order = pymongo.ASCENDING
    if order_choice=='Descending':
        order = pymongo.DESCENDING
    
    index_fields = [
        (user_choice, order)
    ]
    
    sparse_choice = st.radio(label='Choose a sparse', options=['True','False'], horizontal=True)
    unique_choice = st.radio(label='Choose a unique', options=['True','False'], horizontal=True)
    
    sparse = ''
    if sparse_choice=='True':
        sparse=True
    else:
        sparse=False
    
    unique=''
    if unique_choice=='True':
        unique=True
    else:
        unique=False
    
    
    index_options = {
        "unique": unique,
        "sparse": sparse
    }
    
    index_name=''
    try:
        index_name = collection.create_index(index_fields, **index_options)
    except:
        pass
    st.write('Index: ', index_name)
    

def aggregation(query_list):
    print(query_list)
    lst=[]
    if st.button('aggregate'):
        for i in collection.aggregate(query_list):
            lst.append(i)   
        
        df = pd.DataFrame(lst)
        print(df)
        st.dataframe(df.astype('str')) 



st.title('Protein Structure')
df = pd.DataFrame()
collect_name = ''

menu = ["Add / Delete Data", 'Embbeded', 'Update', "Queries"]
choice = st.sidebar.selectbox("Select Option", menu)


if choice == 'Add / Delete Data':
    user_choice = st.radio(label='Choose a collection', options=['Details', 'Sequence'], horizontal=True)
        
    if user_choice == 'Details':
        col1, col2  = st.columns(2)
        
        df = data_upload("Details")
        collect_name = "Details"
        
        collection = db.get_collection("Details")
        
        structureId = col1.text_input('Structure ID')
        classification = col1.text_input('Classification')
        experimentalTechnique = col1.text_input('Experimental Technique')
        macromoleculeType = col1.text_input('Macro Molecule Type')
        residueCount = col1.text_input('Residue Count')
        resolution = col1.slider('Resolution', min_value=0.0, max_value=70.0)
        structureMolecularWeight = col1.text_input('structure Molecular Weight')
        crystallizationMethod = col2.text_input('crystallization Method')
        crystallizationTempK = col2.slider('crystallization Temp K', min_value=0.0, max_value=400.0)
        densityMatthews = col2.slider('density Matthews', min_value=0.0, max_value=100.0)
        densityPercentSol = col2.slider('density Percent Sol', min_value=0.0, max_value=100.0)
        pdbxDetails = col2.text_input('pdbx Details')
        phValue = col2.text_input('phValue')
        publicationYear = col2.text_input('publicationYear')
        
        print(resolution)
        
        if st.button('Insert'):
            st.success('Added Successfully')
            collection.insert_one({'structureId':structureId, 'classification':classification, 'experimentalTechnique':experimentalTechnique, 'resolution':resolution,
                           'macromoleculeType':macromoleculeType, 'residueCount':residueCount, 'structureMolecularWeight':structureMolecularWeight, 'crystallizationMethod':crystallizationMethod
                           , 'crystallizationTempK':crystallizationTempK, 'densityMatthews':densityMatthews
                           , 'densityPercentSol':densityPercentSol, 'pdbxDetails':pdbxDetails, 'phValue':phValue, 'publicationYear':publicationYear, 'Sequence':Embbeded})
            
            
            
    if user_choice == 'Sequence':
        col1, col2 = st.columns(2)
        
        df = data_upload("Sequence")
        collect_name = "Sequence"
        
        collection = db.get_collection("Sequence")
        
        structureId = col1.text_input('Structure ID')
        chainId = col1.text_input('Chain Id')
        sequence = col1.text_input('Sequence')
        residueCount = col2.text_input('Residue Count')
        macromoleculeType = col2.text_input('Macro Molecule Type')
        
        if st.button('Insert'):
            st.success('Added Successfully')
            collection.insert_one({'structureId':structureId, 'chainId':chainId, 'sequence':sequence
                                   , 'residueCount':residueCount, 'macromoleculeType':macromoleculeType})
            
    try:
        record = show(df)
        st.write(record)
        if st.button('Delete'):
            delete_record(record, collect_name)
    except:
        pass
        


elif choice=='Update':
    user_choice = st.radio(label='Choose a collection', options=['Details', 'Sequence'], horizontal=True)
    
    
    if user_choice == 'Details':
        col1, col2  = st.columns(2)
        user_choice = st.radio(label='Choose a cell', options=['structureId','classification','experimentalTechnique',
                           'macromoleculeType', 'residueCount', 'structureMolecularWeight', 'crystallizationMethod',
                           'crystallizationTempK', 'densityMatthews',
                           'densityPercentSol', 'pdbxDetails', 'phValue'], horizontal=True)
        
        update_record("Details", user_choice)
            
    

    if user_choice == 'Sequence':
        col1, col2, col3 = st.columns(3)
        
        user_choice = st.radio(label='Choose a cell', options=['structureId','chainId', 'sequence'
                    , 'residueCount', 'macromoleculeType'], horizontal=True)
        
        
        update_record("Sequence", user_choice)
            
       
            
elif choice=='Embbeded':
    col1, col2 = st.columns(2)
    chainId = col1.text_input('Chain Id')
    sequence = col1.text_input('Sequence')
    residueCount = col2.text_input('Residue Count')
    macromoleculeType = col2.text_input('Macro Molecule Type')
    
    if st.button('Insert'):
        st.success('Added Successfully')
        Embbeded.append({'chainId':chainId, 'sequence':sequence
                                , 'residueCount':residueCount, 'macromoleculeType':macromoleculeType})

    df = pd.DataFrame(Embbeded)
    st.dataframe(df)    
        


elif choice == 'Queries':
    Sequence = st.checkbox(label='Sequence')
    Details = st.checkbox(label='Details')
    lst = []
    
    df.value_counts()
    
    if Details==True and Sequence==False:
        user_query_choice = st.radio(label='Choose a query', options=['Aggregation', 'Find', 'Map Reduce', 'Indexeing'], horizontal=True)
        st.write('--------------------------------------')
        col1, col2, col3, col4  = st.columns(4)
        
        if user_query_choice=='Find':
            collection = db.get_collection('Details')
            
            query = columns()
            
            print(query)
            if st.button('find'):
                try:
                    collected_data = collection.find(query)
                    collect_lst = []
                    for record in collected_data:
                        collect_lst.append(record)
                        
                    print(collect_lst)
                    finded_data = pd.DataFrame(collect_lst)
                    show(finded_data)
                except:
                    pass
            
        
        
        if user_query_choice=='Aggregation':
            query = {}
            query_list = []
            collection = db.get_collection('Details')
            
            match = col1.checkbox(label='match')
            group = col2.checkbox(label='group')
            limit = col3.checkbox(label='limit')
            
            
            if match:
                st.write('------------------------------------------')
                match_dict = columns()
                query_list.append({'$match':match_dict})
            
            
            if group:
                st.write('------------------------------------------')
                operation_choice = st.radio(label='Choose a query', options=['avg', 'count'], horizontal=True)
                
                if operation_choice=='avg':    
                    column_choice = st.radio(label='Choose a column', options=['structureMolecularWeight',
                           'crystallizationTempK', 'densityMatthews',
                           'densityPercentSol', 'phValue'], horizontal=True)
                
                    query_list.append({'$group':{'_id':None,
                                                'Result':{'$avg':'$'+column_choice}
                                                }
                                    })
                    
                if operation_choice=='count':
                    user_choice = st.radio(label='Choose a column', options=['classification','experimentalTechnique',
                           'macromoleculeType', 'crystallizationMethod'], horizontal=True)
                    
                    query_list.append({'$group':{'_id':None,
                                                'count':{'$sum': 1}
                                                }
                                    })
                    
            if limit:
                st.write('------------------------------------------')
                try:
                    limit = st.text_input('enter a positive number')
                    query_list.append({'$limit':int(limit)})
                except:
                    pass
            
            aggregation(query_list)
            
            
        
        if user_query_choice=='Map Reduce':
            collection = db.get_collection('Details')
            operation_choice = st.radio(label='Choose an operation', options=['avg', 'max', 'min'], horizontal=True)
            
            column_choice = st.radio(label='Choose a numeric column', options=['structureMolecularWeight',
                           'crystallizationTempK', 'densityMatthews',
                           'densityPercentSol', 'phValue'], horizontal=True)
            
            user_choice = st.radio(label='Choose a nominal column', options=['classification','experimentalTechnique',
                           'macromoleculeType', 'crystallizationMethod'], horizontal=True)
            
            map_reduce(operation_choice, user_choice, column_choice, collection)
            
            
            
        if user_query_choice == 'Indexeing':
            collection = db.get_collection('Details')
            user_choice = st.radio(label='Choose a column', options=['structureId','classification','experimentalTechnique',
                           'macromoleculeType', 'residueCount', 'structureMolecularWeight', 'crystallizationMethod',
                           'crystallizationTempK', 'densityMatthews',
                           'densityPercentSol', 'pdbxDetails', 'phValue'], horizontal=True)
        
            order_choice=st.radio(label='Choose an order', options=['Ascending', 'Descending'], horizontal=True)

            indexeing(user_choice, order_choice)    



    if Details==False and Sequence==True:
        user_query_choice = st.radio(label='Choose a query', options=['Aggregation', 'Find', 'Map Reduce', 'Indexeing'
                                               ], horizontal=True)
        st.write('--------------------------------------')
        col1, col2, col3, col4  = st.columns(4)
        
        if user_query_choice=='Find':
            collection = db.get_collection('Sequence')
            
            query = {}
            
            structureId_field = col1.checkbox(label='structureId')
            structureId_field_text = col2.text_input(label='structureId')
            
            chainId_field = col1.checkbox(label='chainId')
            chainId_field_text = col3.text_input(label='chainId')
            
            sequence_field = col1.checkbox(label='sequence')
            sequence_field_text = col4.text_input(label='sequence')
            
            residueCount_field = col1.checkbox(label='residueCount')
            residueCount_field_text = col2.text_input(label='residueCount')
            
            if structureId_field:
                query['structureId'] = structureId_field_text
                    
            if chainId_field:
                query['chainId'] = chainId_field_text
            
            if sequence_field:
                query['sequence'] = sequence_field_text
            
            if residueCount_field:
                query['residueCount'] = residueCount_field_text
            
            print(query)
            if st.button('find'):
                try:
                    collected_data = collection.find(query)
                    collect_lst = []
                    for record in collected_data:
                        collect_lst.append(record)
                        
                    finded_data = pd.DataFrame(collect_lst)
                    show(finded_data)
                except:
                    pass
            
                
        if user_query_choice=='Aggregation':
            query = {}
            query_list = []
            collection = db.get_collection('Sequence')
            
            match = col1.checkbox(label='match')
            group = col2.checkbox(label='group')
            limit = col3.checkbox(label='limit')
            
            
            if match:
                st.write('------------------------------------------')
                match_dict = seq_columns()
                query_list.append({'$match':match_dict})
            
            
            if group:
                st.write('------------------------------------------')
                
                operation_choice = st.radio(label='Choose a query', options=['avg', 'count'], horizontal=True)
                if operation_choice=='avg':    
                    query_list.append({'$group':{'_id':None,
                                                'Average Result':{'$avg':'$residueCount'}
                                                }
                                    })
                    
                if operation_choice=='count':
                    query_list.append({'$group':{'_id':None,
                                                'count':{'$sum': 1}
                                                }
                                    })
                    
            
            
            if limit:
                st.write('------------------------------------------')
                try:
                    limit = st.text_input('enter a positive number')
                    query_list.append({'$limit':int(limit)})
                except:
                    pass
            
            
            aggregation(query_list)
            
            
        if user_query_choice=='Map Reduce':
            collection = db.get_collection('Sequence')
            operation_choice = st.radio(label='Choose an operation', options=['avg', 'max', 'min'], horizontal=True)
            
            user_choice = st.radio(label='Choose a nominal column', options=['chainId','sequence',
                           'macromoleculeType'], horizontal=True)
            
            
            map_reduce(operation_choice, user_choice, 'residueCount', collection)
            
                
        if user_query_choice == 'Indexeing':
            collection = db.get_collection('Details')
            user_choice = st.radio(label='Choose a cell', options=['structureId','chainId', 'sequence'
                    , 'residueCount', 'macromoleculeType'], horizontal=True)
        
            order_choice=st.radio(label='Choose an order', options=['Ascending', 'Descending'], horizontal=True)

            indexeing(user_choice, order_choice)
        
    
    if Details==True and Sequence==True:
        ID = st.text_input('Structure ID')
        details = db.get_collection('Details')
        
        if st.button('Show Protien Chain'):
            results = details.aggregate([
            { '$match': { 'structureId': ID} },
            {
                '$lookup':
                {
                    'from': "Sequence",
                    'localField': "structureId",
                    'foreignField': "structureId",
                    'as': "chainId"
                }
            }])
            for i in results:
                
                chain = i['chainId']
                for j in chain:
                    st.write(j['chainId'])
                    
                    
                    
        if st.button('Show Protien Sequence'):
            results = details.aggregate([
            { '$match': { 'structureId': ID} },
            {
                '$lookup':
                {
                    'from': "Sequence",
                    'localField': "structureId",
                    'foreignField': "structureId",
                    'as': "chainId"
                }
            }])
            for i in results:
                
                chain = i['chainId']
                for j in chain:
                    st.write(j['sequence'])
