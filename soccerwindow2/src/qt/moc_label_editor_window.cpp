/****************************************************************************
** Meta object code from reading C++ file 'label_editor_window.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.13)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "label_editor_window.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'label_editor_window.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.13. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_LabelEditorWindow_t {
    QByteArrayData data[18];
    char stringdata0[239];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_LabelEditorWindow_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_LabelEditorWindow_t qt_meta_stringdata_LabelEditorWindow = {
    {
QT_MOC_LITERAL(0, 0, 17), // "LabelEditorWindow"
QT_MOC_LITERAL(1, 18, 12), // "cycleChanged"
QT_MOC_LITERAL(2, 31, 0), // ""
QT_MOC_LITERAL(3, 32, 5), // "cycle"
QT_MOC_LITERAL(4, 38, 19), // "featuresLogSelected"
QT_MOC_LITERAL(5, 58, 8), // "openFile"
QT_MOC_LITERAL(6, 67, 7), // "saveCSV"
QT_MOC_LITERAL(7, 75, 15), // "saveFeaturesLog"
QT_MOC_LITERAL(8, 91, 14), // "selectTimeItem"
QT_MOC_LITERAL(9, 106, 15), // "updateLabelView"
QT_MOC_LITERAL(10, 122, 15), // "selectLabelItem"
QT_MOC_LITERAL(11, 138, 26), // "slotLabelItemDoubleClicked"
QT_MOC_LITERAL(12, 165, 16), // "QTreeWidgetItem*"
QT_MOC_LITERAL(13, 182, 4), // "item"
QT_MOC_LITERAL(14, 187, 6), // "column"
QT_MOC_LITERAL(15, 194, 20), // "slotLabelItemChanged"
QT_MOC_LITERAL(16, 215, 17), // "showFeatureValues"
QT_MOC_LITERAL(17, 233, 5) // "index"

    },
    "LabelEditorWindow\0cycleChanged\0\0cycle\0"
    "featuresLogSelected\0openFile\0saveCSV\0"
    "saveFeaturesLog\0selectTimeItem\0"
    "updateLabelView\0selectLabelItem\0"
    "slotLabelItemDoubleClicked\0QTreeWidgetItem*\0"
    "item\0column\0slotLabelItemChanged\0"
    "showFeatureValues\0index"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_LabelEditorWindow[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      11,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       2,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   69,    2, 0x06 /* Public */,
       4,    0,   72,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       5,    0,   73,    2, 0x08 /* Private */,
       6,    0,   74,    2, 0x08 /* Private */,
       7,    0,   75,    2, 0x08 /* Private */,
       8,    0,   76,    2, 0x08 /* Private */,
       9,    0,   77,    2, 0x08 /* Private */,
      10,    0,   78,    2, 0x08 /* Private */,
      11,    2,   79,    2, 0x08 /* Private */,
      15,    2,   84,    2, 0x08 /* Private */,
      16,    1,   89,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void, QMetaType::Int,    3,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 12, QMetaType::Int,   13,   14,
    QMetaType::Void, 0x80000000 | 12, QMetaType::Int,   13,   14,
    QMetaType::Void, QMetaType::Int,   17,

       0        // eod
};

void LabelEditorWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<LabelEditorWindow *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->cycleChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 1: _t->featuresLogSelected(); break;
        case 2: _t->openFile(); break;
        case 3: _t->saveCSV(); break;
        case 4: _t->saveFeaturesLog(); break;
        case 5: _t->selectTimeItem(); break;
        case 6: _t->updateLabelView(); break;
        case 7: _t->selectLabelItem(); break;
        case 8: _t->slotLabelItemDoubleClicked((*reinterpret_cast< QTreeWidgetItem*(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 9: _t->slotLabelItemChanged((*reinterpret_cast< QTreeWidgetItem*(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 10: _t->showFeatureValues((*reinterpret_cast< const int(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (LabelEditorWindow::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&LabelEditorWindow::cycleChanged)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (LabelEditorWindow::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&LabelEditorWindow::featuresLogSelected)) {
                *result = 1;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject LabelEditorWindow::staticMetaObject = { {
    QMetaObject::SuperData::link<QMainWindow::staticMetaObject>(),
    qt_meta_stringdata_LabelEditorWindow.data,
    qt_meta_data_LabelEditorWindow,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *LabelEditorWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *LabelEditorWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_LabelEditorWindow.stringdata0))
        return static_cast<void*>(this);
    return QMainWindow::qt_metacast(_clname);
}

int LabelEditorWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 11)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 11;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 11)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 11;
    }
    return _id;
}

// SIGNAL 0
void LabelEditorWindow::cycleChanged(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void LabelEditorWindow::featuresLogSelected()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
