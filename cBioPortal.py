# 2015.08.28 08:21:48 ADT
#Embedded file name: /Users/dan/Dropbox/Development/TCGA/cBioPortal.py
__author__ = 'dan'
import requests
import sys
base_url = 'http://www.cbioportal.org/webservice.do?cmd='

def getCancerTypes():
    r = requests.get('%sgetTypesOfCancer' % base_url)
    types = r.text.split('\n')
    return types


def getCancerStudies():
    r = requests.get('%sgetTypesOfCancer' % base_url)
    studies = r.text.split('\n')
    return studies


def getGeneticProfiles(study_id):
    r = requests.get('%sgetGeneticProfiles&cancer_study_id=%s' % (base_url, study_id))
    profiles = r.text.split('\n')
    return profiles


def getCaseList(study_id):
    r = requests.get('%sgetCaseLists&cancer_study_id=%s' % (base_url, study_id))
    results = r.text.split('\n')
    return results


def getMultiProfiles(case_set_id, genetic_profiles, gene):
    genetic_profile_ids = '+'.join(genetic_profiles)
    r = requests.get('%sgetProfileData&case_set_id=%s&genetic_profile_id=%s&gene_list=%s' % (base_url,
     case_set_id,
     genetic_profile_ids,
     gene))
    results = r.text.split('\n')
    clean_results = []
    for result in results:
        if result.startswith('#'):
            pass
        else:
            clean_results.append(result)

    return clean_results


def getMultiGene(case_set_id, genetic_profile_id, genes):
    gene_list = '+'.join(genes)
    sys.stderr.write('Request: %sgetProfileData&case_set_id=%s&genetic_profile_id=%s&gene_list=%s\n' % (base_url,
     case_set_id,
     genetic_profile_id,
     gene_list))
    r = requests.get('%sgetProfileData&case_set_id=%s&genetic_profile_id=%s&gene_list=%s' % (base_url,
     case_set_id,
     genetic_profile_id,
     gene_list))
    results = r.text.split('\n')
    clean_results = []
    for result in results:
        if result.startswith('#'):
            pass
        else:
            clean_results.append(result)

    return clean_results
+++ okay decompyling cBioPortal.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.08.28 08:21:48 ADT
