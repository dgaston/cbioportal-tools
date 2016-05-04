import requests
import sys

base_url = 'http://www.cbioportal.org/webservice.do?cmd='


def get_cancer_types():
    r = requests.get('%sgetTypesOfCancer' % base_url)
    types = r.text.split('\n')

    return types


def get_cancer_studies():
    r = requests.get('%sgetTypesOfCancer' % base_url)
    studies = r.text.split('\n')

    return studies


def get_genetic_profiles(study_id):
    r = requests.get('%sgetGeneticProfiles&cancer_study_id=%s' % (base_url, study_id))
    profiles = r.text.split('\n')

    return profiles


def get_case_list(study_id):
    r = requests.get('%sgetCaseLists&cancer_study_id=%s' % (base_url, study_id))
    results = r.text.split('\n')

    return results


def get_multi_profiles(case_set_id, genetic_profiles, gene):
    genetic_profile_ids = '+'.join(genetic_profiles)
    r = requests.get('%sgetProfileData&case_set_id=%s&genetic_profile_id=%s&gene_list=%s' %
                     (base_url, case_set_id, genetic_profile_ids, gene))
    results = r.text.split('\n')
    clean_results = []
    for result in results:
        if result.startswith('#'):
            pass
        else:
            clean_results.append(result)

    return clean_results


def get_multi_gene(case_set_id, genetic_profile_id, genes):
    gene_list = '+'.join(genes)
    sys.stderr.write('Request: %sgetProfileData&case_set_id=%s&genetic_profile_id=%s&gene_list=%s\n' %
                     (base_url, case_set_id, genetic_profile_id, gene_list))
    r = requests.get('%sgetProfileData&case_set_id=%s&genetic_profile_id=%s&gene_list=%s' %
                     (base_url, case_set_id, genetic_profile_id, gene_list))
    results = r.text.split('\n')
    clean_results = list()
    for result in results:
        if result.startswith('#'):
            continue
        elif not result.strip():
            continue
        else:
            clean_results.append(result)

    return clean_results


def get_clin_data(case_set_id):
    r = requests.get('%sgetClinicalData&case_set_id=%s' % (base_url, case_set_id))
    results = r.text.split('\n')

    return results

