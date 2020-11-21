from modules import modules
from plotter import plotter
from files import files
from importer import importer

# importer.get_success_graph()

paths = [
    'src/main/java/net/sf/jabref/importer/fetcher/ACMPortalFetcher.java'
    # 'src/main/java/net/sf/jabref/importer/ZipFileChooser.java',
    # 'src/main/java/net/sf/jabref/logic/xmp/XMPUtil.java',
    # 'src/main/java/net/sf/jabref/logic/xmp/XMPSchemaBibtex.java',
    # 'src/main/java/net/sf/jabref/gui/preftabs/XmpPrefsTab.java'
]


files.get_graphs(paths)
