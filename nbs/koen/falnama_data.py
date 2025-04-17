import pooch
import tqdm
from glob import glob

Downloader = pooch.create(path=pooch.os_cache("falnama-notebooks"),
            base_url="https://f002.backblazeb2.com/file/falnama-data/datastacks/",
            registry={"WM-71803-01_400_600_50.datastack" : "ee2af34dcbea270de797003500400e7f0655654838bafc880d0943a440283411",
                    "WM-71803-03_250_300_50.datastack" : "ad5bff448f32d4ac4dac46ae6e516af1c96f64e9ced17e3021124f21a5dd4669",
                    "WM-71803-08_250_300_50.datastack" : "14b6ac5fc8acad456ad39b0dd0acbaf6fd9655732a1d11c437fcc0652b753996",
                    "WM-71803-10_250_300_50.datastack" : "5e76db5bfc4b764178e824a7fc6caf5f3e49e64a329dc92691673b5accd0f430",
                    "WM-71803-12_250_300_50.datastack" : "cf0d12cda57a2f348abe1cf29f450131d97e4845d78da20d270a340e9e103db7",
                    "WM-71803-13_400_600_50.datastack" : "e67fd574fa2be48dfaa4cd08feb592c560575a0956cb84d7307760d8de7674c2",
                    "WM-71803-17_400_600_50.datastack" : "83d978ab426844842318cc3a8daf32ab749b1fe81657ca455e0289e94b9ffcf9",
                    "WM-71803-18_400_300_50_det.datastack" : "97bc254b0848172501bf4a96ebf8bd7862e1285607e060bd37cb973cff556226",
                    "WM-71803-18_400_500_50.datastack" : "93f21e5a078f9091a9139ffe8446003ab4eacfcd579221ecccd63b31220dcc27",
                    "WM-71803-19_400_600_50.datastack" : "b0d57800439b2824dfa148510728d18b195167d6f0b38c0539cf11b9bf3176b1",
                    "WM-71803-23_400_600_50.datastack" : "c76b90cd11096b364e7f10fcda67b61459c6ce0bdec0e816d7cc3d4ec70a238f",
                    "WM-71803-24_400_600_50.datastack" : "964603613e2882f570472357a303de232f0afe6a82de692c4ec7d78cb765bd4a",
                    "WM-71803-29_400_500_50.datastack" : "82647269b4b9361f9596f327e64f3b17a1b0512628eb9ed82c344edc796ae26c",
                    "WM-71803-30_250_300_50.datastack" : "af8e1bd23b5cec8e4e710dce050a6ade6bd94660d605650cc6bf27b1fd7d5076",
                    "WM-71803-31_400_600_50.datastack" : "99a747ddf664263f4b1743db0e13657a2e6313fd6aed1088df47c691b6a40c75",
                    "WM-71803-35_400_500_50.datastack" : "9742160af6b274fed19dd5e1b1ab7ef4ffe7c430e9063ee3b0924bb17309a42e"})

def download_all():
    for i, datastack_path in enumerate(Downloader.registry_files):
        total = len(Downloader.registry_files)
        datastack_file = Downloader.fetch(datastack_path, progressbar=True)
        print(f"Checked {i+1}/{total} files")
    print("All data is up to date!")

def get_base_path():
    return Downloader.abspath

def get_datastack_files():
    datastack_files = sorted(glob(f'{Downloader.abspath}/*.datastack', recursive=True))
    return datastack_files
    
