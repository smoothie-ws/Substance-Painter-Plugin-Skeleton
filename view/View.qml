import QtQuick 2.15
import AlgWidgets.Style 2.0

Rectangle {
    width: 400
    height: 400
    color: AlgStyle.background.color.mainWindow

    Column {
        anchors.centerIn: parent
        spacing: 10

        Text {
            text: "Python Plugin"
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            color: AlgStyle.text.color.normal
        }

        Text {
            text: `version: ${Plugin.getPluginVersion()}`
            horizontalAlignment: Text.AlignHCenter
            color: AlgStyle.text.color.normal
        }
    }
}
