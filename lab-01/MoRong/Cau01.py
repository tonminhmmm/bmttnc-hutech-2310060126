
import itertools

def liet_ke_hoan_vi(lst):
    return list(itertools.permutations(lst))

if __name__ == "__main__":
    ds = [1, 2, 3]
    hoan_vis = liet_ke_hoan_vi(ds)
    
    print("Tổng số hoán vị:", len(hoan_vis))
    for hv in hoan_vis:
        print(hv)
