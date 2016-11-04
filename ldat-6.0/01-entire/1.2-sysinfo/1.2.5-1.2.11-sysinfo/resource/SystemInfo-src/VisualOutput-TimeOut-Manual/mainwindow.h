#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <cstdio>
#include <QString>
#include <QMap>

#include <QMainWindow>
#include <QPushButton>
#include <QWidget>
#include <QTabWidget>
#include <QTextBrowser>
#include <QLayout>
#include <QSpacerItem>

namespace Ui {
class MainWindow;
}

struct CommandInfo {
    QString commandType;
    QStringList commandList;
    QStringList commentList;
};

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(int argc,  char *argv[], QWidget *parent = 0 );
    ~MainWindow();
    void initializeLayout();
    void initializeCommandList();
    void createActions();

private slots:
    void changeCommandTypeTabWidget();  // link the button with corresponding tabwidget
    void updateContents(int index);  // link the tabwidget clicked with tab content changing

private:
    bool SpecialCommandType(QString type);
    void OutputSpecialCommandType(QTabWidget * pTabWidget, const struct CommandInfo & specialCommandType);
    void UpdateSpecialCommandType(const struct CommandInfo & specialCommandType);
    bool SpecialCommand(QString command);
    QString OutputSpecialCommand(QString specialCommand);
    void UpdateSpecialCommand(QString keyTabBarTitlle, QString specialCommand);

    void RecordInfotoFile(QString fileName, QString content);  // fileName: base name of the file, join it with info dir path
    void FillNewTab(QTabWidget *parentTabWidget,  QTextBrowser * childTextBrowser, QString barTitle, QString content);
    void UpdateBrowserContent(QString keyTabBarTitle, QString outputContent);

    const int maxEthNumber;
    const int ROW_SPACE;
    const int COLUMN_STRETCH1;
    const int COLUMN_STRETCH2;

    QString outputCommand(QString command);
    QVector<struct CommandInfo> commandInfoList;

//    QStringList outputInfoType;
//    QVector<QStringList> commandList;
//    QVector<QStringList> ;
    QVector<QPushButton *> vPushButtonList;
    QVector<QTabWidget *> vTabWidgetList;
    QMap<QString, QTextBrowser *> mTitleContentList;

    int lastTabWidgetIndex;

    QGridLayout *pGridLayout;
//    QTabWidget * pLastTabWidget;
    QString outputDirPath;
    bool initializeFlag;

    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
