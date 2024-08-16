const { Notification } = require('electron');

// 判断当前系统是否支持通知功能
const isAllowed = Notification.isSupported();
if (isAllowed) {
    // 创建一个通知对象
    const options = {
        title: '��题', // 通知标题
        body: '正文文本，显示在标题下方', // 通知的详细内容
        silent: true, // 系统默认的通知声音
        icon: '', // 通知图标
    }

    // 实例化通知
    const notification = new Notification(options);

    // 为通知添加点击事件监听器
    notification.on('click', () => {  });

    // 为通知添加显示事件监听器
    notification.on('show', () => {  });

    // 为通知添加关闭事件监听器
    notification.on('close', () => {  });

    // 显示通知
    notification.show();
}
