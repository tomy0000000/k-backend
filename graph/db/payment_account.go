package db

import (
    "fmt"
    "gorm.io/gorm"
    "tomy0000000/kman/k-graphql/graph/model"
)

type PaymentAccount struct {
    gorm.Model
    ID    uint
    Name    string
    Transactions    []*Transaction `gorm:"many2many:payment;"`
}

func PaymentAccountFromGraph(pa model.PaymentAccount) PaymentAccount {
    return PaymentAccount{Name: pa.Name}
}

func PaymentAccountToGraph(pa PaymentAccount) model.PaymentAccount {
    graph := model.PaymentAccount{ID: fmt.Sprint(pa.ID), Name: pa.Name}
    return graph
}
