import QtQuick 2.9
import QtQuick.Controls 2.2

ApplicationWindow {
    id: window
    visible: true
    width: 1366
    height: 768

    StackView {
        id: stackView
        initialItem: "ZENWindow.qml"
        anchors.fill: parent

        ZENWindow {
            anchors.fill: parent
        }
    }
}
