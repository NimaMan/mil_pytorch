
import time
import torch 


def train(train_dl, model, epochs=100, learning_rate=5e-4, weight_decay=1e-4, momentum=0.9):

    start = time.time()
    train_losses = []
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, weight_decay=weight_decay, momentum=momentum)
    criterion = torch.nn.BCELoss()

    for epoch in range(epochs): 
        for features, labels in train_dl:
            labels[labels==-1] = 0  # replace -1 classes with Zero
            pred = model(features)
            loss = criterion(pred, labels.float())
            
            # Update weights
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Save loss on this batch
            train_losses.append(loss.float())
        
        # Compute avarega loss on this epoch
        train_loss = torch.mean(torch.tensor(train_losses), dim = 0, keepdim = True)
        # Clear tensor for saving losses over batches
        train_losses = []

    print(f'Finished training - elapsed time: {time.time() - start}')

    return model


def eval_model(model, dataloader):
    model.eval()
    train_acc = []
    pred_probs = [] 
    finalLabels = []
    for features, labels in dataloader:
            labels[labels==-1] = 0  # replace -1 classes with Zero
            pred = model(features)
            pred_probs.append(pred.detach().item())
            train_acc.append(pred.round().detach().item() ==labels.item())
            finalLabels.append(labels.item())

    return sum(train_acc)/len(train_acc), pred_probs,finalLabels
    


    
    
