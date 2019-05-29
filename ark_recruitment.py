class worker(object):
    def __init__(self, name, career, star, tags):
        self.name = name
        self.career = career
        self.star = star
        self.tags = set(tags)
        self.hit_tags = []

    def __str__(self):
        return '{}:{}({}, {:.1f}%)'.format(str(self.star), self.name,  self.career, len(self.hit_tags)*100/len(self.tags))

    def __lt__(self, other):
        return (self.star < other.star)

def main(): 
    f = open("./data/tags.txt")
    text = f.readlines()
    f.close()
    workers = []
    tags_set = set()
    for line in text:
        s_star, s_name, s_career, s_tags, others = line.split(';')
        workers.append(worker(s_name, s_career, int(s_star), s_tags.split(',')+[s_career]))
    for w in workers:
        for tag in w.tags:
            tags_set.add(tag)
    tags_map = {}
    cnt = 1
    for tag in tags_set:
        tags_map[cnt] = tag
        cnt += 1
    print(
    '''
        Welcome to Arknights Recruitment Recommander!
    '''
    )
    for tag in tags_map.items():
        print(tag[0], tag[1])
    print(
    '''
        Please input the the serial numbers of the tag you have and end with -1. 
    '''
    )
    having_tags = set()
    while True:
        tag_number = int(input())
        if (tag_number == -1):
            break
        else:
            having_tags.add(tags_map[tag_number])

    print("You select : " + str(having_tags))
    for tag in having_tags:
        for w in workers:
            if (tag in w.tags):
                w.hit_tags.append(tag)

    ans_dict = {}
    for w in workers:
        w.hit_tags.sort()
        t = tuple(w.hit_tags)
        if (len(t) == 0):
            continue
        if ans_dict.get(t) != None:
            ans_dict[t].append(w)
        else:
            ans_dict[t] = [w]

    import itertools
    addition_dict = {}
    for tags_worker in ans_dict.items():
        tags_len = len(tags_worker[0])
        for i in range(1,tags_len):
            new_l = list(itertools.combinations(tags_worker[0], i))
            for l in new_l:
                t = tuple(l)
                if addition_dict.get(t) != None:
                    addition_dict[t] += tags_worker[1]
                else:
                    addition_dict[t] = list(tags_worker[1])
    

    for tags_worker in addition_dict.items():
        if (ans_dict.get(tags_worker[0]) != None):
            ans_dict[tags_worker[0]] += tags_worker[1]
        else:
            ans_dict[tags_worker[0]] = tags_worker[1]

    for tags_worker in ans_dict.items():
        print(tags_worker[0])
        l = list(set(tags_worker[1]))
        # l = list(tags_worker[1])
        l.sort()
        for w in l:
            print('\t' + str(w))
        print()

if __name__ == '__main__':
    main()