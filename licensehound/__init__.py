import requests
from collections import namedtuple


def get_metadata_json(package):
    url = "https://pypi.python.org/pypi/{}/json".format(package)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def get_trove_classifiers():
    result = requests.get('https://pypi.python.org/pypi?%3Aaction=list_classifiers')
    return result.text.splitlines()


LicensingMetadata = namedtuple('LicensingMetadata',
                               ['version', 'name', 'license', 'maintainer_email', 'author_email',
                                'author', 'license_classifiers'])


MetadataWarning = namedtuple('MetadataWarning',
                             ['field', 'description'])


def get_metadata(package):

    warnings = []
    official_classifiers = get_trove_classifiers()

    json_data = get_metadata_json(package)

    info = json_data['info']

    version = info['version']
    name = info['name']
    license = info.get('license')
    author_email = info.get('author_email')
    maintainer_email = info.get('maintainer_email')
    author = info.get('author')
    classifiers = info.get('classifiers')

    if license is None or license == "":
        warnings.append(
            MetadataWarning(field='license', description='missing license field'))

    license_classifiers = []
    if classifiers is not None:
        license_classifiers = [
            classifier for classifier in classifiers if
            classifier.startswith('License :: ')]
    for license_classifier in license_classifiers:
        if license_classifier not in official_classifiers:
            warnings.append(
                MetadataWarning(field='license classifier',
                                description='Unknown license classifier: {}'.
                                format(license_classifier)))
        elif ":: OSI Approved ::" not in license_classifier:
            warnings.append(
                MetadataWarning(field='license classifier',
                                description='Not OSI approved open source license: {}'.
                                format(license_classifier)))

    if len(license_classifiers) == 0:
        warnings.append(MetadataWarning(field='license_classifiers',
                                        description='No license classifiers present'))

    result = LicensingMetadata(
        version=version,
        name=name,
        license=license,
        author_email=author_email,
        maintainer_email=maintainer_email,
        author=author,
        license_classifiers=license_classifiers
    )
    return result, warnings
