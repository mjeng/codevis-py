import parse_file
import create_graph

testDict={"src1":'\nimport sys\n\nSTAT_START_COL = {"letter": \'F\', "number": 6}\n\ndef get_time():\n    TIME_FORMAT = "%Y-%m-%d"\n    get_time()\n    return strftime(TIME_FORMAT, gmtime())\n\ndef initialize_metadata():\n    METADATA["comics sent"] = METADATA["comics sent"].format(*letters)\n    STAT_START_COL\n    METADATA["MRCN"] = scrape_utils.most_recent_comic_num()\n\ndef run_setup():\n    # CREATE SHEETS].value = md_items[i][1]\n    reset()\n    initialize_metadata()\n\ndef reset():\n    wb = db_client.wb\n    get_time\n\n# NOTE: Doesn\'t run if not specifically running setup - file should only be run once.\nif __name__ == "__main__":\n    print("dummy")\n    reset()\n'
,"src2":'from file1.py import get_time()\n\ndef file2func(arg1, arg2):\n    get_time()\n    pass\n\n\ndef another_func():\n    print()\n    size(variable)\n    while:\n   file2func(arg2, arg1)\n'}
testStr=["src1","src2"]

fml = parse_file.gh_link_entry("https://github.com/mjeng/dummy-repo")
for elem in fml:
	#print(elem.get_func_name()+" --> "+elem.get_call_list())
	print (elem.get_func_name(),'-->',elem.get_times_called(),'-->',elem.get_call_list())
