/****************************************************************************
** Meta object code from reading C++ file 'trainer_dialog.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.13)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "trainer_dialog.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'trainer_dialog.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.13. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_TrainerDialog_t {
    QByteArrayData data[17];
    char stringdata0[194];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_TrainerDialog_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_TrainerDialog_t qt_meta_stringdata_TrainerDialog = {
    {
QT_MOC_LITERAL(0, 0, 13), // "TrainerDialog"
QT_MOC_LITERAL(1, 14, 8), // "executed"
QT_MOC_LITERAL(2, 23, 0), // ""
QT_MOC_LITERAL(3, 24, 15), // "readFieldStatus"
QT_MOC_LITERAL(4, 40, 4), // "open"
QT_MOC_LITERAL(5, 45, 4), // "save"
QT_MOC_LITERAL(6, 50, 15), // "toggleBallCheck"
QT_MOC_LITERAL(7, 66, 2), // "on"
QT_MOC_LITERAL(8, 69, 18), // "toggleBallVelCheck"
QT_MOC_LITERAL(9, 88, 13), // "toggleLeftAll"
QT_MOC_LITERAL(10, 102, 14), // "toggleRightAll"
QT_MOC_LITERAL(11, 117, 15), // "toggleLeftCheck"
QT_MOC_LITERAL(12, 133, 5), // "index"
QT_MOC_LITERAL(13, 139, 16), // "toggleRightCheck"
QT_MOC_LITERAL(14, 156, 21), // "changeAutoRepeatTimer"
QT_MOC_LITERAL(15, 178, 3), // "val"
QT_MOC_LITERAL(16, 182, 11) // "sendCommand"

    },
    "TrainerDialog\0executed\0\0readFieldStatus\0"
    "open\0save\0toggleBallCheck\0on\0"
    "toggleBallVelCheck\0toggleLeftAll\0"
    "toggleRightAll\0toggleLeftCheck\0index\0"
    "toggleRightCheck\0changeAutoRepeatTimer\0"
    "val\0sendCommand"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_TrainerDialog[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      12,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   74,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       3,    0,   75,    2, 0x08 /* Private */,
       4,    0,   76,    2, 0x08 /* Private */,
       5,    0,   77,    2, 0x08 /* Private */,
       6,    1,   78,    2, 0x08 /* Private */,
       8,    1,   81,    2, 0x08 /* Private */,
       9,    1,   84,    2, 0x08 /* Private */,
      10,    1,   87,    2, 0x08 /* Private */,
      11,    1,   90,    2, 0x08 /* Private */,
      13,    1,   93,    2, 0x08 /* Private */,
      14,    1,   96,    2, 0x08 /* Private */,
      16,    0,   99,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Bool,    7,
    QMetaType::Void, QMetaType::Bool,    7,
    QMetaType::Void, QMetaType::Bool,    7,
    QMetaType::Void, QMetaType::Bool,    7,
    QMetaType::Void, QMetaType::Int,   12,
    QMetaType::Void, QMetaType::Int,   12,
    QMetaType::Void, QMetaType::QString,   15,
    QMetaType::Void,

       0        // eod
};

void TrainerDialog::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<TrainerDialog *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->executed(); break;
        case 1: _t->readFieldStatus(); break;
        case 2: _t->open(); break;
        case 3: _t->save(); break;
        case 4: _t->toggleBallCheck((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 5: _t->toggleBallVelCheck((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 6: _t->toggleLeftAll((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 7: _t->toggleRightAll((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 8: _t->toggleLeftCheck((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 9: _t->toggleRightCheck((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 10: _t->changeAutoRepeatTimer((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 11: _t->sendCommand(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (TrainerDialog::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&TrainerDialog::executed)) {
                *result = 0;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject TrainerDialog::staticMetaObject = { {
    QMetaObject::SuperData::link<QDialog::staticMetaObject>(),
    qt_meta_stringdata_TrainerDialog.data,
    qt_meta_data_TrainerDialog,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *TrainerDialog::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *TrainerDialog::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_TrainerDialog.stringdata0))
        return static_cast<void*>(this);
    return QDialog::qt_metacast(_clname);
}

int TrainerDialog::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 12)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 12;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 12)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 12;
    }
    return _id;
}

// SIGNAL 0
void TrainerDialog::executed()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
