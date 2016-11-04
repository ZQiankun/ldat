#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QTimer>

#include <QFile>
#include <QCoreApplication>
#include <QTextStream>

MainWindow::MainWindow(int argc,  char *argv[], QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    maxEthNumber(3),
    ROW_SPACE(3),
    COLUMN_STRETCH1(1),
    COLUMN_STRETCH2(8),
    initializeFlag(true)
{
    ui->setupUi(this);
    this->setWindowTitle("硬件信息汇总");

    initializeCommandList();
    initializeLayout();

    outputDirPath = "";
    if (argc >= 2) { /* For autotest */
        outputDirPath = argv[1];
        QTimer::singleShot(60000, this, SLOT(close()));
    } else { /* For manual operation */
      createActions();
    }
}

void MainWindow::initializeCommandList()
{
    struct CommandInfo commandInfo;
    commandInfo.commandType = QString("硬件信息");
    commandInfo.commandList.clear();
    commandInfo.commandList << "cat /proc/cpuinfo" << "dmidecode | grep -i \'serial number\'" <<"dmidecode -s bios-version" << "fdisk -l" << "df -h" << "hdparm -I /dev/sda";
    commandInfo.commentList.clear();
    commandInfo.commentList << "处理器核心数与频率" << "主板序列号" << "BIOS版本" << "硬盘分区" << "当前硬盘大小" << "硬盘信息及使用情况";
    commandInfoList.append(commandInfo);

    commandInfo.commandType = QString("内存信息");
    commandInfo.commandList.clear();
    commandInfo.commandList << "dmesg | grep mem" << "cat /proc/meminfo";
    commandInfo.commentList.clear();
    commandInfo.commentList << "内存规格" << "内存使用";
    commandInfoList.append(commandInfo);

    // Filter the correct eth number for "ethtool"
    commandInfo.commandType = QString("网卡信息");
    commandInfo.commandList.clear();
    commandInfo.commandList << "dmesg | grep -i \'eth\'" << "ethtool" << "lspci | grep -i \'eth\'";
    commandInfo.commentList.clear();
    commandInfo.commentList << "网卡驱动信息" << "网卡连接信息"<<"网卡控制器信息";
    commandInfoList.append(commandInfo);

    commandInfo.commandType = QString("键鼠信息");
    commandInfo.commandList.clear();
    commandInfo.commandList << "cat /proc/bus/input/devices";
    commandInfo.commentList.clear();
    commandInfo.commentList << "键鼠信息";
    commandInfoList.append(commandInfo);

    commandInfo.commandType = QString("USB设备信息");
    commandInfo.commandList.clear();
    commandInfo.commandList << "lsusb" << "lsusb -v";
    commandInfo.commentList.clear();
    commandInfo.commentList << "USB设备概要" << "USB设备详细信息";
    commandInfoList.append(commandInfo);

    // Filter: integrate all the video information into one page
    commandInfo.commandType = QString("显卡信息");
    commandInfo.commandList.clear();
    commandInfo.commandList << "lspci | grep -i \'VGA\'" << "lspci -v -s `lspci | grep VGA| awk \'{print $1}\'`" << "glxinfo | grep version | grep \"OpenGL version\" ";
    commandInfo.commentList.clear();
    commandInfo.commentList << "显卡控制器信息" << "显卡信息" << "显卡驱动信息";
    commandInfoList.append(commandInfo);

    // Filter: alsamixer-> 声卡芯片信息
    commandInfo.commandType = QString("声卡信息");
    commandInfo.commandList.clear();
    commandInfo.commandList  << "lspci | grep -i audio" << "lsmod | grep sound" << "cat /proc/asound/cards" << "cat /proc/asound/devices" << "cat /proc/asound/hwdep" << "cat /proc/asound/modules" << "cat /proc/asound/version";
    commandInfo.commentList.clear();
    commandInfo.commentList << "声卡型号信息" << "声卡驱动信息" <<  "--cards--" << "--devices--" << "--hwdep--" << "--modules--" << "--version--" ;
    commandInfoList.append(commandInfo);
}

void MainWindow::createActions()
{
    /* Switch tabs */
    for (int i = 0; i < commandInfoList.size() && i < vPushButtonList.size(); ++ i) {
        connect(vPushButtonList.at(i), SIGNAL(clicked()), this, SLOT(changeCommandTypeTabWidget()));
    }

    for (int i = 0; i < commandInfoList.size() && i < vTabWidgetList.size(); ++ i) {
        connect(vTabWidgetList.at(i), SIGNAL(tabBarClicked(int)), this, SLOT(updateContents(int)));
    }
}

void MainWindow::changeCommandTypeTabWidget()
{
    QPushButton * pPushButton = dynamic_cast<QPushButton *>(sender());

    int chooseType = 0;
    for (int i = 0; i < commandInfoList.size(); ++ i) {
        if (QString::compare(pPushButton->text(), commandInfoList.at(i).commandType) == 0) {
            chooseType = i;
            break;
        }
    }

    int rowSize =  commandInfoList.size() + 1;
    pGridLayout->removeWidget(vTabWidgetList.at(lastTabWidgetIndex));
    pGridLayout->addWidget(vTabWidgetList.at(chooseType), 0, 1, rowSize, 1);
    vTabWidgetList.at(lastTabWidgetIndex)->hide();
    vTabWidgetList.at(chooseType)->show();
    lastTabWidgetIndex = chooseType;
//    pLastTabWidget = vTabWidgetList.at(chooseType);
}

void MainWindow::initializeLayout()
{
    pGridLayout = new QGridLayout();

    pGridLayout->setSpacing(2);
    pGridLayout->setMargin(2);
    pGridLayout->setColumnStretch(0, COLUMN_STRETCH1);
    pGridLayout->setColumnStretch(1, COLUMN_STRETCH2);

    int rowSize =  commandInfoList.size() + 1;
    QWidget * pSpaceWidget = new QWidget();
    pSpaceWidget->setMinimumHeight(500);
    for (int i = 0; i < commandInfoList.size(); ++ i) {
        QPushButton * pTypeButton = new QPushButton(commandInfoList.at(i).commandType);
        pTypeButton->setMinimumSize(100, 20);
        vPushButtonList.append(pTypeButton);
        pGridLayout->addWidget(pTypeButton, i, 0, 1, 1);
    }
    pGridLayout->addWidget(pSpaceWidget, rowSize - 1, 0, 1, 1);

    for (int i = 0; i < commandInfoList.size(); ++ i) {
        QTabWidget * pCommandOutputTabWidget = new QTabWidget();
        if (SpecialCommandType(commandInfoList.at(i).commandType)) {
            OutputSpecialCommandType(pCommandOutputTabWidget, commandInfoList.at(i));
        } else {
            for (int j = 0; j < commandInfoList.at(i).commandList.size() && j < commandInfoList.at(i).commentList.size() ; ++ j) {
                QTextBrowser * pOutputBrowser = new QTextBrowser();
                QString command = commandInfoList[i].commandList[j]; // command line
                QString commandOutput = "";
                if (SpecialCommand(command)) {
                    commandOutput = OutputSpecialCommand(command);
                } else {
                    commandOutput = outputCommand(command);
                }

//                pOutputBrowser->setText(commandOutput);
//                pCommandOutputTabWidget->addTab(pOutputBrowser, commandInfoList[i].commentList[j]); // comment
                FillNewTab(pCommandOutputTabWidget, pOutputBrowser, commandInfoList[i].commentList[j], commandOutput);
//                mTitleContentList.insert()
            }
        }
        vTabWidgetList.append(pCommandOutputTabWidget);
    }

    if (vTabWidgetList.size() > 0) {
        QTabWidget *pFirstWidget = vTabWidgetList.at(0);
        pGridLayout->addWidget(pFirstWidget, 0, 1, rowSize, 1);
//        pLastTabWidget = pFirstWidget;
        lastTabWidgetIndex = 0;
    }

    ui->centralWidget->setLayout(pGridLayout);
    initializeFlag = false;
}

void MainWindow::RecordInfotoFile(QString fileName, QString content)
{
//    QString currentPath = QCoreApplication::applicationDirPath();
    QString fileTotalPath = outputDirPath + '/' + fileName;
    printf("currentPath %s, totalPath %s\n", outputDirPath.toStdString().c_str(), fileTotalPath.toStdString().c_str());

    QFile recordFile(fileTotalPath);
    if (!recordFile.open(QIODevice::WriteOnly)) {
        printf("record file open error, %s\n", fileTotalPath.toStdString().c_str());
        return;
    }

    QTextStream in(&recordFile);
    in<< content << "\n";
    recordFile.close();
}

void MainWindow::UpdateSpecialCommand(QString keyTabBarTitlle, QString specialCommand)
{
    QString totalOutput = OutputSpecialCommand(specialCommand);
    UpdateBrowserContent(keyTabBarTitlle, totalOutput);
}

void MainWindow::UpdateBrowserContent(QString keyTabBarTitle, QString outputContent)
{
    QMap<QString, QTextBrowser *>::iterator iter = mTitleContentList.find(keyTabBarTitle);
    iter.value()->setText(outputContent);
}

void MainWindow::UpdateSpecialCommandType(const CommandInfo &specialCommandType)
{
    if (QString::compare(specialCommandType.commandType, "显卡信息") == 0) {
       QString totalOutput = "";
       for (int i = 0; i < specialCommandType.commandList.size(); ++ i) {
           totalOutput += "\n" + specialCommandType.commentList[i] + "\n";
           totalOutput += outputCommand(specialCommandType.commandList[i]);
       }

       UpdateBrowserContent(specialCommandType.commandType, totalOutput);
   } else if (QString::compare(specialCommandType.commandType, "声卡信息") == 0) {
      // 1->1
       for (int i = 0; i < 2; ++ i) {
           QTextBrowser * pOutputBrowser = new QTextBrowser();
           QString outputContents = outputCommand(specialCommandType.commandList[i]);
           UpdateBrowserContent(specialCommandType.commentList[i], outputContents);
       }

       // 1-> *
       QTextBrowser * pOutputBrowser = new QTextBrowser();
       QString totalOutput = "";
       for (int i = 2; i < specialCommandType.commandList.size(); ++ i) {
           totalOutput += "\n" + specialCommandType.commentList[i] + "\n";
           totalOutput += outputCommand(specialCommandType.commandList[i]) + "\n";
       }

       UpdateBrowserContent(specialCommandType.commandType, totalOutput);
   }

}

void MainWindow::updateContents(int index)
{
    QTabWidget * pTabWidget = dynamic_cast<QTabWidget *>(sender());
    QString tabBarTitle = pTabWidget->tabText(index);

    bool findFlag = false;

    for (int i = 0; i < commandInfoList.size(); ++ i) {
        QString tempStr = commandInfoList.at(i).commandType;
        if (QString::compare(tabBarTitle, tempStr) == 0) {
            if (SpecialCommandType(tempStr)) {
                UpdateSpecialCommandType(commandInfoList.at(i));
            }
            break;
        }

        for (int j = 0; j < commandInfoList.at(i).commandList.size() && j < commandInfoList.at(i).commentList.size() ; ++ j) {
            QString tempStr = commandInfoList.at(i).commentList.at(j);
            if (QString::compare(tabBarTitle, tempStr) == 0) {
                QString command = commandInfoList[i].commandList[j]; // command line
                QString commandOutput = "";
                if (SpecialCommand(command)) {
                    UpdateSpecialCommand(tabBarTitle, command);
                } else {
                    commandOutput = outputCommand(command);
                    UpdateBrowserContent(tabBarTitle, commandOutput);
                }
                findFlag = true;
                break;
            }
        }

        if (findFlag) {
            break;
        }
    }
}

QString MainWindow::outputCommand(QString command)
{
    FILE * fp = NULL;
    char buffer[1024];
    QString outputStr = "";

    fp = popen(command.toStdString().c_str(), "r");
    while (NULL != fgets(buffer,sizeof(buffer),fp)) {
        outputStr += QString(buffer);
    }
    pclose(fp);

    return outputStr;
}

bool MainWindow::SpecialCommandType(QString type)
{
    if (QString::compare(type, "显卡信息") == 0) {
        return true;
    } else if (QString::compare(type, "声卡信息") == 0) {
        return true;
    } else {
        return false;
    }
}

// only one tab for some commands
void MainWindow::OutputSpecialCommandType(QTabWidget * pTabWidget, const struct CommandInfo & specialCommandType)
{
     if (QString::compare(specialCommandType.commandType, "显卡信息") == 0) {
        QTextBrowser * pOutputBrowser = new QTextBrowser();
        QString totalOutput = "";
        for (int i = 0; i < specialCommandType.commandList.size(); ++ i) {
            totalOutput += "\n" + specialCommandType.commentList[i] + "\n";
            // TODO: remove "error" information
            totalOutput += outputCommand(specialCommandType.commandList[i]);
        }

//        pOutputBrowser->setText(totalOutput);   // command line
//        pTabWidget->addTab(pOutputBrowser, specialCommandType.commandType); // comment

        FillNewTab(pTabWidget, pOutputBrowser, specialCommandType.commandType, totalOutput);
    } else if (QString::compare(specialCommandType.commandType, "声卡信息") == 0) {
       // 1->1
        for (int i = 0; i < 2; ++ i) {
            QTextBrowser * pOutputBrowser = new QTextBrowser();
            QString command = specialCommandType.commandList[i]; // command line
            QString ouputContents = outputCommand(command);

//            pOutputBrowser->setText(outputCommand(command));
//            pTabWidget->addTab(pOutputBrowser, specialCommandType.commentList[i]); // comment

            FillNewTab(pTabWidget, pOutputBrowser, specialCommandType.commentList[i], ouputContents);
        }

        // 1-> *
        QTextBrowser * pOutputBrowser = new QTextBrowser();
        QString totalOutput = "";
        for (int i = 2; i < specialCommandType.commandList.size(); ++ i) {
            totalOutput += "\n" + specialCommandType.commentList[i] + "\n";
            totalOutput += outputCommand(specialCommandType.commandList[i]) + "\n";
        }

        FillNewTab(pTabWidget, pOutputBrowser, specialCommandType.commandType, totalOutput);
//        pOutputBrowser->setText(totalOutput);   // command line
//        pTabWidget->addTab(pOutputBrowser, specialCommandType.commandType); // comment
    }
}

void MainWindow::FillNewTab(QTabWidget *parentTabWidget, QTextBrowser *childTextBrowser, QString barTitle, QString content)
{
    childTextBrowser->setText(content);   // command line
    parentTabWidget->addTab(childTextBrowser, barTitle); // comment
    mTitleContentList.insert(barTitle, childTextBrowser);

    // add at 2015/04/23, to output result into files
    if (initializeFlag && !outputDirPath.isEmpty()) { // add content at the first time to fill tabwidgets
        QString fileName  = barTitle;
        RecordInfotoFile(fileName,  content);
    }
    // add at 2015/04/23, to output result into files, end
}

bool MainWindow::SpecialCommand(QString command)
{
    if (command.contains("ethtool")) {
        return true;
    } else {
        return false;
    }
}

QString MainWindow::OutputSpecialCommand(QString specialCommand)
{
    QString totalOutput = "";
    if (specialCommand.contains("ethtool")) {
        QString testOuput = outputCommand("ifconfig | awk -F \"[: ]\" \'BEGIN{RS = \'\\n\'} {if (($0 ~ /.*BROADCAST.*/) && ($0 ~ /.*MULTICAST.*/) && ($0 ~/.*UP.*/)&& ($0 !~/.*LOOPBACK.*/)) {print $1}}\'");
        QString ethName = testOuput.simplified();
        totalOutput = outputCommand("ethtool " + ethName);
    }

    return totalOutput;
}

MainWindow::~MainWindow()
{
    delete ui;
}
