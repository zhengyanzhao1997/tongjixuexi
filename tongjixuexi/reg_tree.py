import numpy as np
class Node:
    def __init__(self,feature_index=None,cut_value=None,y_value=None,left_l=None,right_s=None):
        self.feature_index=feature_index
        self.y_value=y_value
        self.cut_value=cut_value
        self.left_l=left_l
        self.right_s=right_s

class Cart_reg:
    def __init__(self,X,Y,min_leave_data=3):
        self.min_leave_data = min_leave_data
        self.root=Node()
        self.X = X
        self.Y = Y
        self.feature_num = len(X[0])

    def cauclate_loss(self,Y1,Y2):
        if len(Y1)!=0 and len(Y2)!=0:
            sum_1 = sum([(y - np.mean(Y1))**2 for y in Y1])
            sum_2 = sum([(y - np.mean(Y2))**2 for y in Y2])
            return sum_1 + sum_2
        elif len(Y1)!=0:
            return sum([(y - np.mean(Y1))**2 for y in Y1])
        elif len(Y2)!=0:
            return sum([(y - np.mean(Y1))** 2 for y in Y2])

    def find_spilt(self,X,Y):
        X = np.array(X)
        Y = np.array(Y)
        save_loss = []
        save_feature = []
        save_value = []
        for i in range(self.feature_num):
            list_ix = np.array([x[i] for x in X])
            for j in list_ix:
                loss_ = self.cauclate_loss(Y[list_ix <= j],Y[list_ix > j])
                save_loss.append(loss_)
                save_feature.append(i)
                save_value.append(j)
        min_loss = min(save_loss)
        min_index = save_loss.index(min_loss)
        min_feature = save_feature[min_index]
        min_value = save_value[min_index]
        return min_feature,min_value

    def build_tree(self):
        def build_tree_(node, X, Y):
            X = np.array(X)
            Y = np.array(Y)
            # print(len(X))
            if len(X) <= self.min_leave_data:
                node.y_value=np.mean(Y)
                return
            min_feature,min_value = self.find_spilt(X,Y)
            node.feature_index = min_feature
            node.cut_value = min_value
            large_index = np.array([x[min_feature] for x in X])>min_value
            small_index = np.array([x[min_feature] for x in X])<=min_value
            X_left = X[large_index]
            X_right = X[small_index]
            Y_left = Y[large_index]
            Y_right = Y[small_index]
            node.left_l = Node()
            node.right_s = Node()
            build_tree_(node.left_l,X_left,Y_left)
            build_tree_(node.right_s,X_right,Y_right)
        build_tree_(self.root,self.X,self.Y)

    def print_tree(self):
        root = self.root
        def pre_order(root):
            if root:
                print(root.feature_index,root.cut_value,root.y_value)
                pre_order(root.left_l)
                pre_order(root.right_s)
        pre_order(root)

    def predict_single(self,X):
        if len(X) != self.feature_num:
            raise IndexError
        node = self.root
        while node.y_value is None:
            if X[node.feature_index] <= node.cut_value:
                node = node.right_s
            else:
                node = node.left_l
        return node.y_value

    def predict(self,X):
        X = np.array(X)
        if len(X.shape) == 1:
            return self.predict_single(X)
        else:
            result = []
            for i in X:
                result.append(self.predict_single(i))
        return result