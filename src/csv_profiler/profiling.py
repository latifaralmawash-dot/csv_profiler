
MISSING = {"","na","n/a","null","none","nan"}

def is_missing(value:str | None) ->bool :
    if value is None:
        return True
    return value.strip().casefold() in MISSING
def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None




def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]

    if not usable:
        return "text"

    for v in usable:
        if try_float(v) is None:
            return "text"

    return "number"


def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing(v)]
    nums = [try_float(v) for v in usable]

    count = len(nums)

    return {
        "count": count,
        "missing": len(values) - count,
        "unique": len(set(nums)),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / count
    }




from collections import Counter

def profile_row(rows: list[dict[str, str]]) -> dict:
    if not rows: return {"n_rows": 0, "n_columns": 0, "columns": []}
    
    n_rows = len(rows)
    column_names = list(rows[0].keys()) 

    col_profiles = []
    for col in column_names:
        values = [i.get(col, "") for i in rows]
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        unique = len(set(usable))

        profile = {
            "name": col,
            "type": infer_type(values), 
            "missing": missing,
            "missing pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": unique
        }
        col_profiles.append(profile)

    return {"n_rows": n_rows, "n_colums": len(column_names), "columns": col_profiles}



# test
print(infer_type(["latifa", "7"]))   # text

print(infer_type(["latifa", "rashed"])) #text
print(infer_type(["7", "10"]))       # number



print(numeric_stats(["10", "", "20", "na", "30"]))


   





