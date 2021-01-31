import pickle


def dump_object(object, path):
    with open(path, 'wb') as f:
        pickle.dump(object, f, protocol=2)


def load_object(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj
