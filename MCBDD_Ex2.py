from chembl_webresource_client.new_client import new_client
import requests, sys


molecule = new_client.molecule
target = new_client.target
mechanism = new_client.mechanism
approvedDrugs_byName = molecule.filter(max_phase = 4).only('pref_name','first_approval').order_by('pref_name')
"""print(approvedDrugs_byName)"""
approvedDrugs_byDate = molecule.filter(max_phase = 4).only('pref_name','first_approval').order_by('first_approval')
"""print(approvedDrugs_byDate)"""
drug = []


#retrieves all drugs from 2019 up to 2025
for i in range (2019,2026):
    approvedDrugs_2019_andNewer = molecule.filter(max_phase = 4,first_approval = i).only('molecule_chembl_id','pref_name','first_approval').order_by('first_approval')
    for j in approvedDrugs_2019_andNewer:
        drug_id = j.get('molecule_chembl_id')
        name = j.get('pref_name')
        year = j.get('first_approval')
        
        # this is important as we can't just use the pref name from molecules
        #this is because pref_name is not unique so we need to connect target
        #and mechanism that we can connect the right endpoints so we connect 
        #molecule_chembl_id -> mechanism -> fetch target id in mechanism -> target

        mechanisms = mechanism.filter(molecule_chembl_id = drug_id)
        uniprots = []
        
        for chembl_target_id in mechanisms:
            target_id = chembl_target_id.get('target_chembl_id')
            if target_id != None:
                #gets us everything from target associated with given target_id 
                temp_target = target.get(target_id)
                #this will get us all the target_components for a given id 
                target_list = temp_target.get('target_components',[])
                for comps in target_list:
                    #fetches the accesion number if the component is protein
                    if comps['component_type'] == "PROTEIN":
                            uniprots.append(comps['accession'])
        
        drug.append({'ID': drug_id,'Name': name, 'Year': year, 'Uniprots': uniprots})
           


#prits all drugs from 2019 to 2025
# for i in range (len(drug)):
#      print(drug[i])
    
# prints all key words for every uniprot accesion number by seding a request
# to the uniprot protein api     
respond_collection = []
for i in range (len(drug)):
    uniprots_list = drug[i]['Uniprots']
    for j in range(len(uniprots_list)):
        allkeywords =[]
        respond_list = []
        requestURL = requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/"
        requestURL += uniprots_list[j]
        r = requests.get(requestURL, headers={ "Accept" : "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        responseBody = r.json()
        keywords = responseBody.get('keywords', [])
        for key in keywords:
            allkeywords.append(key['value'])
        respond_list.append({'ID': drug_id,'Name': name, 'Year': year,'Uniprots': uniprots_list[j] ,'keywords': allkeywords})
        #print( keywords)
    respond_collection.append(respond_list)

print(respond_collection)



            
        


