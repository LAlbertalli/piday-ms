import cPickle as pickle
from math import ceil
from sklearn import svm, linear_model

data_sets = ["data/%d.db"%i for i in xrange(5)]

def load_data(data_sets):
    ret = []
    for filename in data_sets:
        with open(filename,"rb") as f:
            data = pickle.load(f)
            diffs = [[(j['rec'] - j['sent']).total_seconds() for j in i] for i in data]
            data_in = [i[:3] for i in diffs]
            label = [i[3] for i in diffs]
            label_noavg = [i[3]+sum(i[:3])/3 for i in diffs]
            ret.append((data_in, label, label_noavg))
    return ret

def make_train_test(data,label,kfold):
    if len(data) != len(label):
        raise Exception("Data and label must have the same size")
    l = len(data)
    t = int(ceil(1.*l/kfold))
    for i in xrange(0,l,t):
        training = ([],[])
        testing = ([],[])
        v = range(len(data))
        for i in xrange(i,min(i+t,l)):
            testing[0].append(data[i])
            testing[1].append(label[i])
            v.remove(i)
        for i in v:
            training[0].append(data[i])
            training[1].append(label[i])
        yield training, testing

def make_regression(tool_f,args,kwargs,training, testing, linear = False):
    tool = tool_f(*args,**kwargs)
    tool.fit(*training)
    if linear:
        errors = [tool.predict(i) - j for i,j in zip(*testing)]
    else:
        errors = [tool.predict(i)[0] - j for i,j in zip(*testing)]
    return errors

def confidence(errors,delta = 3):
    errors = map(lambda x:abs(x), errors)
    avg = sum(errors)/len(errors)
    std = (sum((i - avg)**2 for i in errors)/len(errors))**0.5
    return avg - delta*std, avg, avg+delta*std, on_target_num(errors)

def gold_standard(data, delta = 3):
    return confidence(data[1], delta)

def on_target_num(data):
    return 100. * len(filter(lambda x:abs(x) < 0.001, data))/len(data)

def test(data, kfold, mean, tool_f, args, kwargs, linear, testname):
    errors = []
    for training, testing in make_train_test(data[0],data[1 if mean else 2],kfold):
        errors += make_regression(tool_f, args, kwargs, training, testing, linear)
    print("Test %s: range = [%6f, %6f, %6f], success = %1f%%"%((testname,) + confidence(errors)))

tests = [
    ('linear', True, linear_model.LinearRegression,True,(),{}),
    ('linear_m', True,linear_model.LinearRegression,False,(),{}),
    ('lasso', True, linear_model.LinearRegression,True,(),{}),
    ('lasso_m',True, linear_model.LinearRegression,False,(),{}),
    ('svm',False, svm.SVR,True,(),{}),
    ('svm_m',False, svm.SVR,False,(),{}),
    ]

def all_tests(tests, data, kfold):
    print("Gold Standard: range = [%6f, %6f, %6f], success = %1f%%"%gold_standard(data))
    for testname, linear, tool_f, mean, args, kwargs in tests:
        test(data, kfold, mean, tool_f, args, kwargs, linear, testname)

