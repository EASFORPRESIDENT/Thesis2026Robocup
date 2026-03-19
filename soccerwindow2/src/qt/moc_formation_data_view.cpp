/****************************************************************************
** Meta object code from reading C++ file 'formation_data_view.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.13)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "formation_data_view.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'formation_data_view.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.13. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_FormationDataView_t {
    QByteArrayData data[22];
    char stringdata0[263];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_FormationDataView_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_FormationDataView_t qt_meta_stringdata_FormationDataView = {
    {
QT_MOC_LITERAL(0, 0, 17), // "FormationDataView"
QT_MOC_LITERAL(1, 18, 12), // "dataSelected"
QT_MOC_LITERAL(2, 31, 0), // ""
QT_MOC_LITERAL(3, 32, 3), // "idx"
QT_MOC_LITERAL(4, 36, 20), // "indexChangeRequested"
QT_MOC_LITERAL(5, 57, 15), // "old_shown_index"
QT_MOC_LITERAL(6, 73, 15), // "new_shown_index"
QT_MOC_LITERAL(7, 89, 15), // "deleteRequested"
QT_MOC_LITERAL(8, 105, 12), // "ballReplaced"
QT_MOC_LITERAL(9, 118, 1), // "x"
QT_MOC_LITERAL(10, 120, 1), // "y"
QT_MOC_LITERAL(11, 122, 14), // "playerReplaced"
QT_MOC_LITERAL(12, 137, 4), // "unum"
QT_MOC_LITERAL(13, 142, 14), // "setCurrentData"
QT_MOC_LITERAL(14, 157, 16), // "QTreeWidgetItem*"
QT_MOC_LITERAL(15, 174, 7), // "current"
QT_MOC_LITERAL(16, 182, 19), // "menuChangeDataIndex"
QT_MOC_LITERAL(17, 202, 14), // "menuDeleteData"
QT_MOC_LITERAL(18, 217, 21), // "changeCoordinateValue"
QT_MOC_LITERAL(19, 239, 11), // "QModelIndex"
QT_MOC_LITERAL(20, 251, 5), // "index"
QT_MOC_LITERAL(21, 257, 5) // "value"

    },
    "FormationDataView\0dataSelected\0\0idx\0"
    "indexChangeRequested\0old_shown_index\0"
    "new_shown_index\0deleteRequested\0"
    "ballReplaced\0x\0y\0playerReplaced\0unum\0"
    "setCurrentData\0QTreeWidgetItem*\0current\0"
    "menuChangeDataIndex\0menuDeleteData\0"
    "changeCoordinateValue\0QModelIndex\0"
    "index\0value"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_FormationDataView[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       9,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       5,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   59,    2, 0x06 /* Public */,
       4,    2,   62,    2, 0x06 /* Public */,
       7,    1,   67,    2, 0x06 /* Public */,
       8,    3,   70,    2, 0x06 /* Public */,
      11,    4,   77,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
      13,    1,   86,    2, 0x08 /* Private */,
      16,    0,   89,    2, 0x08 /* Private */,
      17,    0,   90,    2, 0x08 /* Private */,
      18,    2,   91,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void, QMetaType::Int,    3,
    QMetaType::Void, QMetaType::Int, QMetaType::Int,    5,    6,
    QMetaType::Void, QMetaType::Int,    3,
    QMetaType::Void, QMetaType::Int, QMetaType::Double, QMetaType::Double,    3,    9,   10,
    QMetaType::Void, QMetaType::Int, QMetaType::Int, QMetaType::Double, QMetaType::Double,    3,   12,    9,   10,

 // slots: parameters
    QMetaType::Void, 0x80000000 | 14,   15,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 19, QMetaType::Double,   20,   21,

       0        // eod
};

void FormationDataView::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<FormationDataView *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->dataSelected((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 1: _t->indexChangeRequested((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 2: _t->deleteRequested((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->ballReplaced((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< double(*)>(_a[2])),(*reinterpret_cast< double(*)>(_a[3]))); break;
        case 4: _t->playerReplaced((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< double(*)>(_a[3])),(*reinterpret_cast< double(*)>(_a[4]))); break;
        case 5: _t->setCurrentData((*reinterpret_cast< QTreeWidgetItem*(*)>(_a[1]))); break;
        case 6: _t->menuChangeDataIndex(); break;
        case 7: _t->menuDeleteData(); break;
        case 8: _t->changeCoordinateValue((*reinterpret_cast< const QModelIndex(*)>(_a[1])),(*reinterpret_cast< double(*)>(_a[2]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (FormationDataView::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FormationDataView::dataSelected)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (FormationDataView::*)(int , int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FormationDataView::indexChangeRequested)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (FormationDataView::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FormationDataView::deleteRequested)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (FormationDataView::*)(int , double , double );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FormationDataView::ballReplaced)) {
                *result = 3;
                return;
            }
        }
        {
            using _t = void (FormationDataView::*)(int , int , double , double );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&FormationDataView::playerReplaced)) {
                *result = 4;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject FormationDataView::staticMetaObject = { {
    QMetaObject::SuperData::link<QTreeWidget::staticMetaObject>(),
    qt_meta_stringdata_FormationDataView.data,
    qt_meta_data_FormationDataView,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *FormationDataView::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *FormationDataView::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_FormationDataView.stringdata0))
        return static_cast<void*>(this);
    return QTreeWidget::qt_metacast(_clname);
}

int FormationDataView::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QTreeWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 9;
    }
    return _id;
}

// SIGNAL 0
void FormationDataView::dataSelected(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void FormationDataView::indexChangeRequested(int _t1, int _t2)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t2))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void FormationDataView::deleteRequested(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void FormationDataView::ballReplaced(int _t1, double _t2, double _t3)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t2))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t3))) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}

// SIGNAL 4
void FormationDataView::playerReplaced(int _t1, int _t2, double _t3, double _t4)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t2))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t3))), const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t4))) };
    QMetaObject::activate(this, &staticMetaObject, 4, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
