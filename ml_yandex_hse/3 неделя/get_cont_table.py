f = open('classification.csv', encoding='utf-8').readlines()
TP = 0
TN = 0
FP = 0
FN = 0

for line in f[1:]:
    true, pred = line.strip('\n').split(',')
    if true == pred:
        if true == '1':
            TP += 1
        else:
            TN += 1
    else:
        if pred == '1':
            FP += 1
        else:
            FN += 1

print('TP - {}, TN - {}, FP - {}, FN - {}'.format(TP, TN, FP, FN))

