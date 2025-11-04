> [!WARNING]
> The UMSR is in the process of replacing NSE4 with more robust systems. This process is expected to conclude by 2027 with the introduction of NSE5. Development on NSE4 will continue until its complete phase out. Versions 4.1, 4.2, and 4.3 are planned for release between late 2025 and early 2027 and will include a subset of features from NSE5. The development process of NSE4 going forward may be best described as "patchwork" as it will be focussed mostly on porting new UMSR financial technologies and requirements (e.g., [SMIFT](https://github.com/Minecraft-Interserver-Trade-Org/SMIFT-Documentation)) and **NOT** on stability and code quality. Features may also be _removed_ in later 4.x releases.

<p align="center">
    <h1 align="center">NSE4 Core</h1>
    <p align="center">
        NSE4 is an exchange management system developed by members of the UMSR Minecraft Server used among players to trade in in-game financial markets dealing in equities, derivatives, and commodities.
    </p>
</p>

<div align="center">
    <img src=".github/markets.png", width="800">
</div>

## What is the UMSR?
The UMSR is a private Minecraft Server founded in 2019 with the goal of developing an efficient in-game economic and political system which facilitates growth and reduces time spent on subjectively bording tasks thanks to enhanced [division of labor](https://en.wikipedia.org/wiki/Division_of_labour). The server implements a free market economy with its own currency, central bank, government, corporations, and financial markets.

## Why NSE4?
From 2020 to 2023, players used a proprietary market management system. However, the system needed to be repalced due to software shortcomings and had to be rewritten from the ground up. NSE4, formerly knnown as NSE Market System, is the fourth version of the above-mentioned exchange system and the first open source one.   

In-game financial markets enhance liquidity and reduce overall volatility in the economy, allowing for more rapid growth and more efficient allocation of resources. This is especially visibile in the case of commodities markets, which have contributed grately to price stability and liquidity since the introduction of NSE4 on the UMSR server.

## Features of NSE4 Core
- Market data visualization in tables and charts
- Limit and Market Orders
- Order cancelation
- Real time order matching
- Session management and settlement
- Separation of transaction processing and settlement
- Easy instant transfer of assets and deposits between accounts
- JSON API over TCP (Using UNet and MCom)

## Performance considerations
Performance may varry wildly between "maker" orders and "taker" orders. Maker orders provide liquidity to the marketplace, whereas taker orders take away liquidity. Practically, maker orders are limit orders with price and/or size characteristics that make them umnatchable at the time of issuance, while taker orders are limit or market orders with size and price levels that allow them to be matched instantly.
To the user, the process of placing an order is the same regardless of it being "maker" or "taker", but NSE4 handles them very differently.
Maker orders are just checked for price and size, and added to the order book, while taker orders are matched, checked for how much liquidity they take, and partialy cleared. In some cases, taker orders may require the entire market depth map to be recalculated.

Another factor in regards to performance are "lazy" orders, i.e. asynchronous orders issued with the `lazy` command, which means the client does not need to wait for confirmation before issuing other orders. They're meant for HFTs and program traders, and take the same time to be processed, but due to their non-blocking behavior, the rate is mostly determined by connection speed and client efficiency.

## Disclaimer
This software is meant to be used exclusively n the context of in-game economies, and may not omply with real world regulations such as those of the SEC (Securities Exchange Commission), MIFID (Markets in Financial Instruments Directive), or other regulatory frameworks. Given its private nature and the short development time, it also lacks many security features which may make it incompatible with privacy and data security regulations such as GDPR.

NSE4 is designed to work on the UMSR Minecraft Server with in-game money and assets, in complience with in-game regulations and rules around financial markets and under the supervision of in-game regulatory institutions. Use it at your own risk, neither the author of the software, nor the UMSR Minecraft Server and its members take any responsibility. As per the LICENSE agreement detailed in the LICENSE file, the software is not guaranteed for fitness either.
