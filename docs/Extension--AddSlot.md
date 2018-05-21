Extension —— AddSlot

slot 是Scrapy的 downloader 组件中重要的一块，

用来控制 并发数和下载延时。



![](http://p2a2srwhl.bkt.clouddn.com/2018-01-16-055016.png)

默认的 slot 如上图所示， Scrapy 的 `CONCURRENT_REQUESTS`控制全局的并发，

`CONCURRENT_REQUESTS_PER_DOMAIN` 和 `CONCURRENT_REQUESTS_PER_IP` 则控制每一个 slot 的并发。

也就是说，在默认情况下，==一个网站域名/IP产生一个 slot。一个 slot 控制一个网站的并发。==

但是在编写爬虫的过程中，可能会需要对同一个域名不同的请求分别创建不同的 slot，比如有部分请求需要设置 延时，而另外的请求不需要设置延时。这时候就有了 `AddSlot` 扩展。

![](http://p2a2srwhl.bkt.clouddn.com/2018-01-16-070626.png)

如上图所示，自定义的 slot并发和延时都是自定义的，在Request.meta 中添加`download_slot`为 your_slot1或your_slot2 就生效了。



## AddSlot



### ADDSLOT_ENABLED: 

Default: `False`

### SLOTS:

Default: `None`

添加自定义 SLOT
eg.

```Python
SLOTS = {
        'your_slot1': {'concurrency': 2, 'delay': 0},  # 设置并发为2，延时为0的 SLOT
        'your_slot2': {'concurrency': 3, 'delay': 1}  # 设置并发为3，延时为1的 SLOT
     } 
```
注意事项： CONCURRENT_REQUESTS是全局并发数，  slot 并发会受到全局并发的限制，因此请设置全局并发数大于 slot 并发数的总和。

