import QtQuick 2.4

Item {
    width: 250
    height: 20

    property alias spmText: spmText
    property alias xText: xText
    property alias yText: yText
    property alias zfText: zfText
    property alias zlText: zlText
    property alias angText: angText

    Rectangle {
        id: spmCol
        x: 0
        y: 0
        width: 50
        color: "#ffffff"
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
        color: "#ffffff"
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
        color: "#ffffff"
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
        id: zfCol
        width: 50
        color: "#ffffff"
        anchors.top: yCol.top
        anchors.topMargin: 0
        anchors.bottom: yCol.bottom
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        Text {
            id: zfText
            x: 14
            y: 3
            text: qsTr("Zf")
            font.pixelSize: 12
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
        anchors.left: yCol.right
        border.width: 1
    }

    Rectangle {
        id: zlCol
        y: -2
        width: 50
        color: "#ffffff"
        anchors.topMargin: 0
        anchors.leftMargin: 0
        anchors.top: yCol.top
        Text {
            id: zlText
            x: 14
            y: 3
            text: qsTr("Zl")
            font.pixelSize: 12
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
        anchors.left: zfCol.right
        anchors.bottom: yCol.bottom
        anchors.bottomMargin: 0
        border.width: 1
    }

    Rectangle {
        id: angCol
        width: 50
        color: "#ffffff"
        anchors.topMargin: 0
        anchors.leftMargin: 0
        anchors.top: zlCol.top
        Text {
            id: angText
            x: 14
            y: 3
            text: qsTr("ang")
            font.pixelSize: 12
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }
        anchors.left: zlCol.right
        anchors.bottom: zlCol.bottom
        anchors.bottomMargin: 0
        border.width: 1
    }
}
