import json
from pprint import pprint
import numpy as np

from matplotlib.pyplot import cla
from data import data
from classify import classify

# data.store_data()


# x_train, y_train, x_test, y_test = classify.get_train_test()

# classify.train(x_train, y_train)

# x = np.append(x_train, x_test, axis=0)
# y = np.append(y_train, y_test, axis=0)

# classify.test(x_test, y_test)


# good = [
#     'src/main/java/net/sf/jabref/gui/groups/GroupSelector.java',
#     'src/main/java/net/sf/jabref/gui/openoffice/OOBibBase.java',
#     'src/main/java/net/sf/jabref/logic/formatter/casechanger/CaseKeeperList.java',
#     'src/main/java/net/sf/jabref/bst/VM.java',
#     'src/main/java/net/sf/jabref/model/entry/BibLatexEntryTypes.java',
# ]

bad = [
    'src/main/java/net/sf/jabref/JabRefPreferences.java',
    'src/main/java/net/sf/jabref/Globals.java',
    'src/main/java/net/sf/jabref/gui/BasePanel.java',
    'src/main/java/net/sf/jabref/pdfimport/PdfImporter.java',
    'src/main/java/net/sf/jabref/logic/openoffice/OpenOfficePreferences.java',
    'src/main/java/net/sf/jabref/logic/cleanup/CleanupPreset.java',
    'src/main/java/net/sf/jabref/logic/l10n/Localization.java',
    'src/main/java/net/sf/jabref/gui/help/HelpFiles.java',
    'src/main/java/net/sf/jabref/logic/config/SaveOrderConfig.java',
    'src/main/java/net/sf/jabref/gui/IconTheme.java',
    'src/main/java/net/sf/jabref/gui/undo/NamedCompound.java',
    'src/main/java/net/sf/jabref/MetaData.java',
    'src/main/java/net/sf/jabref/exporter/ExportFormats.java',
    'src/main/java/net/sf/jabref/specialfields/SpecialFieldsUtils.java',
    'src/main/java/net/sf/jabref/logic/util/UpdateField.java',
    'src/main/java/net/sf/jabref/gui/JabRefFrame.java',
    'src/main/java/net/sf/jabref/specialfields/Rank.java',
    'src/main/java/net/sf/jabref/logic/net/ProxyPreferences.java',
    'src/main/java/net/sf/jabref/importer/EntryFromFileCreator.java',
    'src/main/java/net/sf/jabref/specialfields/SpecialFieldValue.java',
    'src/main/java/net/sf/jabref/logic/labelpattern/LabelPatternUtil.java'
]

t, d = classify.__read_data()

# x = classify.__create_x_array(d, good, 333)

# classes = classify.predict(x)

# pprint(dict(zip(good, classes)))

x = classify.__create_x_array(d, bad, 333)

classes = classify.predict(x)

for b, c in zip(bad, classes):

    if not c:
        print(b)
