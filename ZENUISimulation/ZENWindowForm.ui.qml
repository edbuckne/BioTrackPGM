import QtQuick 2.4
import QtQuick.Controls 2.5

Item {
    id: element
    width: 1366
    height: 768

    Item {
        id: xPos
        x: 130
        y: 443
        width: 184
        height: 35

        Rectangle {
            id: xPosRect
            y: 5
            height: 20
            color: "#ffffff"
            anchors.left: parent.left
            anchors.leftMargin: 80
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.verticalCenter: parent.verticalCenter
            border.width: 1

            TextInput {
                id: xPosInput
                text: qsTr("")
                font.family: "Times New Roman"
                anchors.leftMargin: 5
                anchors.fill: parent
                font.pixelSize: 12
                selectByMouse: true
            }
        }

        Text {
            id: xPosText
            x: 7
            y: 8
            text: qsTr("X Position:")
            anchors.verticalCenter: xPosRect.verticalCenter
            anchors.right: xPosRect.left
            anchors.rightMargin: 5
            font.pixelSize: 12
        }
    }

    Item {
        id: yPos
        x: 130
        width: 184
        height: 35
        anchors.right: xPos.right
        anchors.rightMargin: 0
        anchors.top: xPos.bottom
        anchors.topMargin: 0
        Rectangle {
            id: yPosRect
            y: 5
            height: 20
            color: "#ffffff"
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.leftMargin: 80
            anchors.verticalCenter: parent.verticalCenter
            TextInput {
                id: yPosInput
                text: qsTr("")
                anchors.fill: parent
                font.pixelSize: 12
                font.family: "Times New Roman"
                anchors.leftMargin: 5
                selectByMouse: true
            }
            anchors.left: parent.left
            border.width: 1
        }

        Text {
            id: yPosText
            x: 7
            y: 8
            text: qsTr("Y Position:")
            anchors.right: yPosRect.left
            font.pixelSize: 12
            anchors.rightMargin: 5
            anchors.verticalCenter: yPosRect.verticalCenter
        }
    }

    Item {
        id: zPos
        x: 130
        y: 2
        width: 184
        height: 35
        anchors.right: yPos.right
        anchors.topMargin: 0
        anchors.rightMargin: 0
        anchors.top: yPos.bottom
        Rectangle {
            id: zPosRect
            y: 5
            height: 20
            color: "#ffffff"
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.leftMargin: 80
            anchors.verticalCenter: parent.verticalCenter
            TextInput {
                id: zPosInput
                text: qsTr("")
                anchors.fill: parent
                font.pixelSize: 12
                font.family: "Times New Roman"
                anchors.leftMargin: 5
                selectByMouse: true
            }
            anchors.left: parent.left
            border.width: 1
        }

        Text {
            id: zPosText
            x: 7
            y: 8
            text: qsTr("Z Position:")
            anchors.right: zPosRect.left
            font.pixelSize: 12
            anchors.rightMargin: 5
            anchors.verticalCenter: zPosRect.verticalCenter
        }
    }

    ScrollView {
        id: specBox
        width: 235
        height: 200
        anchors.top: xPos.top
        anchors.topMargin: 0
        anchors.left: xPos.right
        anchors.leftMargin: 50

        Rectangle {
            id: rectangle
            x: 0
            width: 300
            color: "#ffffff"
            anchors.bottom: parent.bottom
            anchors.top: parent.top
            border.width: 1

            Rectangle {
                id: spmCol
                x: 0
                y: 0
                width: 50
                color: "#f0f0f0"
                border.width: 1
                anchors.bottom: parent.top
                anchors.bottomMargin: -20
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 0

                Text {
                    id: spmText
                    x: 14
                    y: 3
                    text: qsTr("SPM")
                    font.pixelSize: 12
                }
            }

            Rectangle {
                id: xCol
                x: 50
                y: 0
                width: 50
                color: "#f0f0f0"
                anchors.topMargin: 0
                anchors.leftMargin: 0
                anchors.top: parent.top
                Text {
                    id: xText
                    x: 14
                    y: 3
                    text: qsTr("X")
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 12
                }
                anchors.left: spmCol.right
                anchors.bottom: parent.top
                anchors.bottomMargin: -20
                border.width: 1
            }

            Rectangle {
                id: yCol
                x: 116
                width: 50
                color: "#f0f0f0"
                anchors.top: xCol.top
                anchors.topMargin: 0
                anchors.bottom: xCol.bottom
                anchors.bottomMargin: 0
                anchors.leftMargin: 0
                Text {
                    id: yText
                    x: 14
                    y: 3
                    text: qsTr("Y")
                    font.pixelSize: 12
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                anchors.left: xCol.right
                border.width: 1
            }

            Rectangle {
                id: z1Col
                width: 50
                color: "#f0f0f0"
                anchors.top: yCol.top
                anchors.topMargin: 0
                anchors.bottom: yCol.bottom
                anchors.bottomMargin: 0
                anchors.leftMargin: 0
                Text {
                    id: z1Text
                    x: 14
                    y: 3
                    text: qsTr("Z1")
                    font.pixelSize: 12
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                anchors.left: yCol.right
                border.width: 1
            }

            Rectangle {
                id: z2Col
                y: -2
                width: 50
                color: "#f0f0f0"
                anchors.topMargin: 0
                anchors.leftMargin: 0
                anchors.top: yCol.top
                Text {
                    id: z2Text
                    x: 14
                    y: 3
                    text: qsTr("Z2")
                    font.pixelSize: 12
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                anchors.left: z1Col.right
                anchors.bottom: yCol.bottom
                anchors.bottomMargin: 0
                border.width: 1
            }

            Rectangle {
                id: angCol
                width: 50
                color: "#f0f0f0"
                anchors.topMargin: 0
                anchors.leftMargin: 0
                anchors.top: z2Col.top
                Text {
                    id: angText
                    x: 14
                    y: 3
                    text: qsTr("Ang")
                    font.pixelSize: 12
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                anchors.left: z2Col.right
                anchors.bottom: z2Col.bottom
                anchors.bottomMargin: 0
                border.width: 1
            }

            ListView {
                id: listView
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.top: spmCol.bottom
                anchors.topMargin: 0
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 0
                delegate: SpecimenDelegate {
                    spmText.text: spm
                    xText.text: xT
                    yText.text: yT
                    zfText.text: z1
                    zlText.text: z2
                }
                model: ListModel {
                    id: listModel

                    ListElement {
                        spm: "1"
                        xT: "421"
                        yT: "897"
                        z1: "4213"
                        z2: "4389"
                    }
                }
            }
        }
    }

    Button {
        id: addButton
        y: 407
        width: 50
        height: 20
        text: qsTr("Add")
        focusPolicy: Qt.NoFocus
        anchors.left: specBox.left
        anchors.leftMargin: 35
        anchors.bottom: specBox.top
        anchors.bottomMargin: 15
    }

    Text {
        id: zFirstLabel
        x: 168
        text: qsTr("Z First:")
        anchors.top: zPos.bottom
        anchors.topMargin: 20
        font.pixelSize: 12
    }

    Text {
        id: zFirstText
        y: 568
        text: qsTr("")
        anchors.verticalCenter: zFirstLabel.verticalCenter
        anchors.left: zFirstLabel.right
        anchors.leftMargin: 5
        font.pixelSize: 12
    }

    Text {
        id: zLastLabel
        x: 168
        y: 8
        text: qsTr("Z Last:")
        anchors.right: zFirstLabel.right
        anchors.rightMargin: 0
        font.pixelSize: 12
        anchors.topMargin: 40
        anchors.top: zPos.bottom
    }

    Text {
        id: zLastText
        x: 8
        y: 576
        width: 2
        text: qsTr("")
        anchors.verticalCenterOffset: 0
        font.pixelSize: 12
        anchors.leftMargin: 5
        anchors.verticalCenter: zLastLabel.verticalCenter
        anchors.left: zLastLabel.right
    }

    Button {
        id: zFirstButton
        x: 110
        y: 566
        width: 52
        height: 19
        text: qsTr("Set Zf")
        anchors.right: zFirstLabel.left
        anchors.rightMargin: 10
        anchors.verticalCenter: zFirstLabel.verticalCenter
    }

    Button {
        id: zLastButton
        x: 105
        y: 565
        width: 52
        height: 19
        text: qsTr("Set Zl")
        anchors.right: zFirstButton.right
        anchors.rightMargin: 0
        anchors.verticalCenter: zLastLabel.verticalCenter
    }

    Button {
        id: removeAllButton
        x: -5
        y: 408
        width: 77
        height: 20
        text: qsTr("Remove All")
        focusPolicy: Qt.NoFocus
        anchors.bottomMargin: 0
        anchors.left: addButton.right
        anchors.bottom: addButton.bottom
        anchors.leftMargin: 10
    }

    Item {
        id: ang
        x: 130
        y: 408
        width: 184
        height: 35
        anchors.bottom: xPos.top
        anchors.bottomMargin: 0
        Rectangle {
            id: angRect
            y: 5
            height: 20
            color: "#ffffff"
            anchors.rightMargin: 0
            anchors.left: parent.left
            TextInput {
                id: angInput
                text: qsTr("")
                anchors.fill: parent
                anchors.leftMargin: 5
                font.pixelSize: 12
                font.family: "Times New Roman"
                selectByMouse: true
            }
            border.width: 1
            anchors.right: parent.right
            anchors.leftMargin: 80
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            id: angTextLabel
            x: 7
            y: 8
            text: qsTr("Angle:")
            anchors.rightMargin: 5
            anchors.right: angRect.left
            font.pixelSize: 12
            anchors.verticalCenter: xPos1Rect.verticalCenter
        }
    }

    Button {
        id: startButton
        x: 210
        y: 78
        text: qsTr("Start Experiment")
        anchors.bottom: xPos.top
        anchors.bottomMargin: 325
        anchors.horizontalCenter: xPos.horizontalCenter
    }
}
