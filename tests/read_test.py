import FastClick.FactorRead as fread

if __name__ == "__main__":
    factor = "factor_big_table12"
    res = fread.factor_read(factor, "2005-01-01", "2020-01-01", [])
    print(res)