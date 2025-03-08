/**
 * File: log.ts
 * Author: Wesley
 */
type SizeOption = number | string;
type StyleConfig = {
  color?: string;
  size?: SizeOption;
  background?: string;
  lineHeight?: string | number;
};

class AutoLogger {
  private styles: string[];
  private hasLogged = false;

  constructor(private message: string) {
    this.styles = [];
    // 添加最终输出保险机制
    this.scheduleFlush();
  }

  private scheduleFlush() {
    setTimeout(() => {
      if (!this.hasLogged) {
        this.flush();
      }
    }, 100);
  }

  private flush() {
    if (this.hasLogged) return;
    this.hasLogged = true;
    console.info(`%c${this.message}`, this.styles.join('; '));
  }

  private addStyle(property: string, value: string) {
    if (property === 'line-height') {
      this.styles.push('display: inline-block');
    }
    this.styles.push(`${property}: ${value}`);
    // 简化Proxy处理
    return new Proxy(this, {
      get: (target, prop) => {
        if (typeof prop === 'symbol') return;
        if (prop in target) {
          return (target as any)[prop];
        }
        this.flush();
        return undefined;
      },
    });
  }

  background(color: string) {
    const isValid = this.validateColor(color);
    if (!isValid) console.warn(`Invalid background: ${color}`);
    return isValid ? this.addStyle('background', color) : this;
  }

  lineHeight(height: string | number) {
    let value: string;

    // 处理无单位数字（视为倍数）
    if (typeof height === 'number' && height > 0) {
      const fontSize =
        this.styles
          .find((s) => s.startsWith('font-size:'))
          ?.split(':')[1]
          ?.replace('px', '') || '16'; // 默认16px
      value = `${Number(fontSize) * height}px`;
    } else {
      value = typeof height === 'number' ? `${height}px` : height;
    }

    return this.addStyle('line-height', value);
  }

  private validateColor(color: string) {
    const colorRegex = /^(#([\da-f]{3}){1,2}|rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(,\s*[\d.]+)?\s*\))$/i;
    return colorRegex.test(color);
  }
}

class ConsoleLogger {
  private createLogger(msg: string, color: string, size?: SizeOption) {
    const logger = new AutoLogger(msg);
    logger['addStyle']('color', color);
    if (size !== undefined) {
      const fontSize = typeof size === 'number' ? `${size}px` : size;
      logger['addStyle']('font-size', fontSize);
    }
    return logger;
  }

  black(msg: string, size?: SizeOption) {
    return this.createLogger(msg, '#000000', size);
  }

  green(msg: string, size?: SizeOption) {
    return this.createLogger(msg, '#07c160', size);
  }

  blue(msg: string, size?: SizeOption) {
    return this.createLogger(msg, '#1890ff', size);
  }

  yellow(msg: string, size?: SizeOption) {
    return this.createLogger(msg, 'rgb(255,152,0)', size);
  }

  red(msg: string, size?: SizeOption) {
    return this.createLogger(msg, '#fa5151', size);
  }

  custom(msg: string, options: StyleConfig) {
    const { color = '#000000', size } = options;
    const logger = this.createLogger(msg, color, size);
    if (options.background) logger.background(options.background);
    if (options.lineHeight) logger.lineHeight(options.lineHeight);
    return logger;
  }

  warn(message: string) {
    console.warn(`⚠️ ${message}`);
  }

  error(message: string) {
    console.error(`❌ ${message}`);
  }
}

export const log = new ConsoleLogger();
