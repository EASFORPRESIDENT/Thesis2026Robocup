/****************************************************************************
** Meta object code from reading C++ file 'simple_label_selector.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.13)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "simple_label_selector.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'simple_label_selector.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.13. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_SimpleLabelSelector_t {
    QByteArrayData data[13];
    char stringdata0[137];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_SimpleLabelSelector_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_SimpleLabelSelector_t qt_meta_stringdata_SimpleLabelSelector = {
    {
QT_MOC_LITERAL(0, 0, 19), // "SimpleLabelSelector"
QT_MOC_LITERAL(1, 20, 13), // "cycleSelected"
QT_MOC_LITERAL(2, 34, 0), // ""
QT_MOC_LITERAL(3, 35, 14), // "rcsc::GameTime"
QT_MOC_LITERAL(4, 50, 1), // "t"
QT_MOC_LITERAL(5, 52, 7), // "saveCSV"
QT_MOC_LITERAL(6, 60, 7), // "openCSV"
QT_MOC_LITERAL(7, 68, 11), // "selectLabel"
QT_MOC_LITERAL(8, 80, 5), // "label"
QT_MOC_LITERAL(9, 86, 23), // "onTableSelectionChanged"
QT_MOC_LITERAL(10, 110, 11), // "QModelIndex"
QT_MOC_LITERAL(11, 122, 5), // "index"
QT_MOC_LITERAL(12, 128, 8) // "previous"

    },
    "SimpleLabelSelector\0cycleSelected\0\0"
    "rcsc::GameTime\0t\0saveCSV\0openCSV\0"
    "selectLabel\0label\0onTableSelectionChanged\0"
    "QModelIndex\0index\0previous"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_SimpleLabelSelector[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       5,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   39,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       5,    0,   42,    2, 0x08 /* Private */,
       6,    0,   43,    2, 0x08 /* Private */,
       7,    1,   44,    2, 0x08 /* Private */,
       9,    2,   47,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void, 0x80000000 | 3,    4,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    8,
    QMetaType::Void, 0x80000000 | 10, 0x80000000 | 10,   11,   12,

       0        // eod
};

void SimpleLabelSelector::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<SimpleLabelSelector *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->cycleSelected((*reinterpret_cast< const rcsc::GameTime(*)>(_a[1]))); break;
        case 1: _t->saveCSV(); break;
        case 2: _t->openCSV(); break;
        case 3: _t->selectLabel((*reinterpret_cast< const int(*)>(_a[1]))); break;
        case 4: _t->onTableSelectionChanged((*reinterpret_cast< const QModelIndex(*)>(_a[1])),(*reinterpret_cast< const QModelIndex(*)>(_a[2]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (SimpleLabelSelector::*)(const rcsc::GameTime & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimpleLabelSelector::cycleSelected)) {
                *result = 0;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject SimpleLabelSelector::staticMetaObject = { {
    QMetaObject::SuperData::link<QMainWindow::staticMetaObject>(),
    qt_meta_stringdata_SimpleLabelSelector.data,
    qt_meta_data_SimpleLabelSelector,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *SimpleLabelSelector::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *SimpleLabelSelector::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_SimpleLabelSelector.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int SimpleLabelSelector::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 5)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 5;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 5)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 5;
    }
    return _id;
}

// SIGNAL 0
void SimpleLabelSelector::cycleSelected(const rcsc::GameTime & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
