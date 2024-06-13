from sklearn import metrics


def summarize(y_test, y_pred):
  print(metrics.classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))
  print(performance(y_test, y_pred))
  print(metrics.confusion_matrix(y_test, y_pred))


def performance(y_test, y_pred):
  return {'acc': metrics.accuracy_score(y_test, y_pred), 'roc_auc': metrics.roc_auc_score(y_test, y_pred),
          'f1': metrics.f1_score(y_test, y_pred), 'precision': metrics.precision_score(y_test, y_pred),
          'recall': metrics.recall_score(y_test, y_pred)}
