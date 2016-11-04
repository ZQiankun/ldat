#include "mainwindow.h"
#include <QApplication>
//#include <QTextCodec>  /* Add for Qt4 */

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

/* Add for Qt4 */
//    QTextCodec *codec = QTextCodec::codecForName("UTF-8");
//    QTextCodec::setCodecForLocale(codec);
//    QTextCodec::setCodecForTr(codec);
//    QTextCodec::setCodecForCStrings(codec);

    MainWindow w(argc, argv);
    w.show();

    return a.exec();
}
