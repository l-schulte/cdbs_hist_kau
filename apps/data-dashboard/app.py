from modules import modules
from files import files
from importer import importer

# importer.get_success_graph()

f = [
    {'good': True, 'path': 'src/main/java/net/sf/jabref/gui/groups/GroupSelector.java'},
    {'good': True, 'path': 'src/main/java/net/sf/jabref/gui/openoffice/OOBibBase.java'},
    {'good': True, 'path': 'src/main/java/net/sf/jabref/logic/formatter/casechanger/CaseKeeperList.java'},
    {'good': True, 'path': 'src/main/java/net/sf/jabref/bst/VM.java'},
    {'good': True, 'path': 'src/main/java/net/sf/jabref/model/entry/BibLatexEntryTypes.java'},
    {'good': False, 'path': 'src/main/java/net/sf/jabref/JabRefPreferences.java'},
    {'good': False, 'path': 'src/main/java/net/sf/jabref/Globals.java'},
    {'good': False, 'path': 'src/main/java/net/sf/jabref/gui/BasePanel.java'},
    {'good': False, 'path': 'src/main/java/net/sf/jabref/pdfimport/PdfImporter.java'},
    {'good': False, 'path': 'src/main/java/net/sf/jabref/logic/openoffice/OpenOfficePreferences.java'},
]


# files.get_graphs_per_file(f)
files.get_graphs_per_metric(f)
