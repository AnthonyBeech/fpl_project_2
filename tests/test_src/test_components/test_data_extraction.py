import os
import shutil

from src.components.data_extraction import LegacyDataExtractor

years = [20, 21]
source_dir = "tests/test_data/legacy/20yy_yy/players"
extract_dir = "tests/test_data/legacy/exdir"
tmp_dir = "tests/test_data/legacy/tmpdir"
file_pattern = "*/gw.csv"

legacy_dir = "tests/test_data/legacy"
legacy_hide_dir = "tests/test_data/hidden"


def test_legacy_data_extractor():
    extractor = LegacyDataExtractor(
        years, source_dir, extract_dir, tmp_dir, file_pattern
    )
    extractor.make_dirs()
    assert os.path.exists(extract_dir) and os.path.exists(tmp_dir)

    extractor.extract_gw_data()
    print(extractor.players)
    assert extractor.players == {"fname1_lname1"}

    extractor.combine_extracted_data()
    extracted_csv1 = "tests/test_data/legacy/exdir/fname_lname.csv"
    extracted_csv2 = "tests/test_data/legacy/exdir/fname1_lname1.csv"
    assert os.path.exists(extracted_csv1) and os.path.exists(extracted_csv2)

    extractor.cleanup()
    assert not os.path.exists(tmp_dir)
