from train_model import load_model

def test_model(text):
    
    model = load_model()
    prediction = (model.predict(text) > 0.5).astype(int)
    return prediction
