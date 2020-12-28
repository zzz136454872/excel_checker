
def rm_chinese(a):
    end_chinese=-1
    for i in range(len(a)):
        if ord(a[i])>256:
            end_chinese=i
    return a[end_chinese+1:]

if __name__ == '__main__':
    a='基于K-medoids的改进PBFT共识机制 (Improved PBFT Consensus Mechanism Based on K-medoids).'
    print(rm_chinese(a))

