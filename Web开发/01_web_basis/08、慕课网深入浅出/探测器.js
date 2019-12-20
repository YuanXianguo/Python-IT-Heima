// 实践-探测器

// 定义一个立即执行匿名函数包装变量，防止泄露
!function (window) {
    function DetectorBase(configs) {
        // 只有通过new创建实例调用，而不能直接调用，(new调用返回this)
        if(!this instanceof DetectorBase){
            throw new Error("Do not invoke without new.");
        }
        this.configs = configs;
        this.analyze();
    }

    // 定义一个基类抽象方法，并提示需要被继承
    DetectorBase.prototype.detect = function () {
        throw new Error("Not implemented");
    };

    // 定义analyze方法
    DetectorBase.prototype.analyze = function () {
        console.log("analyzing...");
        this.data = "###data###";
    };

    // 定义链接探测器子类
    function LinkDetector(links) {
        if(!this instanceof LinkDetector){
            throw new Error("Do not invoke without new.");
        }
        this.links = links;
        // 调用父类的方法
        DetectorBase.apply(this, arguments);
    }

    // 定义容器探测器子类
    function ContainerDetector(containers) {
        if(!this instanceof ContainerDetector){
            throw new Error("Do not invoke without new.");
        }
        this.containers = containers;
        DetectorBase.apply(this, arguments);
    }

    // 先继承，再扩展
    inherit(LinkDetector, DetectorBase);
    inherit(ContainerDetector, DetectorBase);

    LinkDetector.prototype.detect = function () {
        console.log("Loading data:" + this.data);
        console.log("Link detection started.");
        console.log("Scaning links:"+ this.links);
    };

    ContainerDetector.prototype.detect = function () {
        console.log("Loading data:" + this.data);
        console.log("Container detection started.");
        console.log("Scaning containers:" + this.containers);
    };

    // 防止被修改
    Object.freeze(DetectorBase);
    Object.freeze(DetectorBase.prototype);
    Object.freeze(LinkDetector);
    Object.freeze(LinkDetector.prototype);
    Object.freeze(ContainerDetector);
    Object.freeze(ContainerDetector.prototype);

    // 将三个类暴漏在全局，同时保护不可修改
    Object.defineProperties(window, {
        LinkDetector:{value:LinkDetector},
        ContainerDetector:{value:ContainerDetector},
        DetectorBase:{value:DetectorBase}
    });

    // 定义继承函数
    function inherit(subClass, superClass) {
        subClass.prototype = Object.create(superClass.prototype);
        subClass.prototype.constructor = subClass;
    }
}(this);

// test
var cd = new ContainerDetector("#abc#");
var ld = new LinkDetector("http://www.baidu.com");

cd.detect();
ld.detect();
