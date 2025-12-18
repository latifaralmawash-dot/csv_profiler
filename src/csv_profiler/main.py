def main():
    args = sys.argv 
    report = profile_row(data) 
    with open("report.json", "w") as f:
        json.dump(report, f) 
    print("Done! ")



        











