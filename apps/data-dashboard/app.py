from modules import modules
from files import files
from importer import importer

# importer.get_success_graph()

# f = [
#     {'good': True, 'path': 'src/main/java/net/sf/jabref/gui/groups/GroupSelector.java'},
#     {'good': True, 'path': 'src/main/java/net/sf/jabref/gui/openoffice/OOBibBase.java'},
#     {'good': True, 'path': 'src/main/java/net/sf/jabref/logic/formatter/casechanger/CaseKeeperList.java'},
#     {'good': True, 'path': 'src/main/java/net/sf/jabref/bst/VM.java'},
#     {'good': True, 'path': 'src/main/java/net/sf/jabref/model/entry/BibLatexEntryTypes.java'},
#     {'good': False, 'path': 'src/main/java/net/sf/jabref/JabRefPreferences.java'},
#     {'good': False, 'path': 'src/main/java/net/sf/jabref/Globals.java'},
#     {'good': False, 'path': 'src/main/java/net/sf/jabref/gui/BasePanel.java'},
#     {'good': False, 'path': 'src/main/java/net/sf/jabref/pdfimport/PdfImporter.java'},
#     {'good': False, 'path': 'src/main/java/net/sf/jabref/logic/openoffice/OpenOfficePreferences.java'},
# ]

f = [
    {"good": False, "path": "src/main/java/net/sf/jabref/JabRefPreferences.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/Globals.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/gui/BasePanel.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/pdfimport/PdfImporter.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/logic/openoffice/OpenOfficePreferences.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/logic/cleanup/CleanupPreset.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/logic/l10n/Localization.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/gui/help/HelpFiles.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/logic/config/SaveOrderConfig.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/gui/IconTheme.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/gui/undo/NamedCompound.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/MetaData.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/exporter/ExportFormats.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/specialfields/SpecialFieldsUtils.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/logic/util/UpdateField.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/gui/JabRefFrame.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/specialfields/Rank.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/logic/net/ProxyPreferences.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/importer/EntryFromFileCreator.java"},
    {"good": False, "path": "src/main/java/net/sf/jabref/specialfields/SpecialFieldValue.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/groups/GroupSelector.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/openoffice/OOBibBase.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/logic/formatter/casechanger/CaseKeeperList.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/bst/VM.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/model/entry/BibLatexEntryTypes.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/preftabs/TableColumnsTab.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/keyboard/EmacsKeyBindings.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/openoffice/OpenOfficePanel.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/journals/ManageJournalsPanel.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/plaintextimport/TextInputDialog.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/logic/util/strings/HTMLUnicodeConversionMaps.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/importer/fileformat/MedlineHandler.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/fieldeditors/FileListEditor.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/openoffice/StyleSelectDialog.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/maintable/MainTableSelectionListener.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/mergeentries/MergeEntries.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/importer/fileformat/PdfContentImporter.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/groups/GroupDialog.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/ContentSelectorDialog2.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/search/SearchResultsDialog.java"},
    {"good": True, "path": "src/main/java/net/sf/jabref/gui/EntryCustomizationDialog.java"}
]


# files.get_graphs_per_file(f)
files.get_graphs_per_metric(f)
# importer.get_success_graph()
