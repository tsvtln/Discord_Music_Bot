-- GIFs table
CREATE TABLE IF NOT EXISTS gifs (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(64) NOT NULL,
    gif_url TEXT NOT NULL,
    nsfw BOOLEAN NOT NULL DEFAULT FALSE,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO gifs (category, gif_url) VALUES
('beer','https://media.giphy.com/media/wKSnAdyvKHKHS/giphy.gif'),
('beer','https://media.giphy.com/media/lTGLOH7ml3poQ6JoFg/giphy.gif'),
('beer','https://media.giphy.com/media/QTgzmGzanMnhiwsBql/giphy.gif'),
('beer','https://media.giphy.com/media/l0HlTocc7w1xFoz6g/giphy.gif'),
('beer','https://media.giphy.com/media/1esoXMqqOjYGm5Bdqt/giphy.gif'),
('beer','https://media.giphy.com/media/9GJ2w4GMngHCh2W4uk/giphy.gif'),
('beer','https://media.giphy.com/media/zTB68FHqA6VRS/giphy.gif'),
('beer','https://media.giphy.com/media/3oEjHNSN9EhhBi2QJq/giphy.gif'),
('beer','https://media4.giphy.com/media/26tP21xUQnOCIIoFi/giphy.gif'),
('beer','https://media.giphy.com/media/2AM7sBtPHGTL5r5WFV/giphy.gif'),
('beer','https://media3.giphy.com/media/AJmrZl2TrH2lvtwwQw/giphy.gif');

INSERT INTO gifs (category, gif_url) VALUES
('cheer','https://media.giphy.com/media/Zw3oBUuOlDJ3W/giphy.gif'),
('cheer','https://media.giphy.com/media/4Tkagznwgrv6A4asQb/giphy.gif'),
('cheer','https://media.giphy.com/media/l0ExgfAdB2Z9V35hS/giphy.gif'),
('cheer','https://media.giphy.com/media/RBx8fOTbEmC8iy27Ki/giphy.gif'),
('cheer','https://media.giphy.com/media/TujSrrPYXqeAdPnvuh/giphy.gif'),
('cheer','https://media.giphy.com/media/GvlQffBPPLygHFd43p/giphy.gif'),
('cheer','https://media.giphy.com/media/hfKTf4RvJJRHL70Zvo/giphy.gif'),
('cheer','https://media.giphy.com/media/l0MYHCPKJ9H2VmRyg/giphy.gif'),
('cheer','https://media.giphy.com/media/dXFd3q0msGpMjgNEls/giphy.gif'),
('cheer','https://media.giphy.com/media/cEYFeDYAEZ974cOS8CY/giphy.gif');

INSERT INTO gifs (category, gif_url, nsfw) VALUES
('booba','https://media4.giphy.com/media/28A92fQr8uG6Q/giphy.gif',TRUE),
('booba','https://media.giphy.com/media/HjlKKc14d5tBK/giphy.gif',TRUE),
('booba','https://media.giphy.com/media/l378p60yRSCeVoyAM/giphy.gif',TRUE),
('booba','https://media2.giphy.com/media/QscGFjzLHXVg4/giphy.gif',TRUE),
('booba','https://media.giphy.com/media/9R2C1v4Y91pp6/giphy.gif',TRUE),
('booba','https://media.giphy.com/media/Q1Q2BRA7CXDGg/giphy.gif',TRUE),
('booba','https://media.giphy.com/media/tQrweyYjPGPjq/giphy.gif',TRUE);

INSERT INTO gifs (category, gif_url, nsfw) VALUES
('kur','https://media4.giphy.com/media/Qc8GJi3L3Jqko/giphy.gif',TRUE),
('kur','https://media.giphy.com/media/zCOY3loJHTnfG/giphy.gif',TRUE),
('kur','https://media.giphy.com/media/okEAjcVdCLl4I/giphy.gif',TRUE),
('kur','https://media.giphy.com/media/1fkdaiYSkzKGM2a3Wj/giphy.gif',TRUE),
('kur','https://media.giphy.com/media/l3vRhvmSOagowtJ96/giphy.gif',TRUE),
('kur','https://media.giphy.com/media/ybpps0dQwaXf2/giphy.gif',TRUE);

INSERT INTO gifs (category, gif_url) VALUES
('usl','https://media.giphy.com/media/dQ5XTlqXTysQdGVdWB/giphy.gif'),
('usl','https://media.giphy.com/media/6JSihSBLPqS1VhO9i2/giphy.gif'),
('usl','https://media.giphy.com/media/iScdi2qu0xfGr8chJq/giphy.gif'),
('usl','https://media.giphy.com/media/R9cQo06nQBpRe/giphy.gif'),
('usl','https://media.giphy.com/media/Gtnf8Fok8An9m/giphy.gif');

INSERT INTO gifs (category, gif_url) VALUES
('its_wednesday','https://64.media.tumblr.com/47d8fcdc9ff224e4621a07acd605848a/tumblr_ou5pz8N1kh1wubnyeo1_r1_250.gif');

INSERT INTO gifs (category, gif_url) VALUES
('not_wednesday','https://preview.redd.it/wukhr6ylhjo41.png?width=640&crop=smart&auto=webp&s=6d249d495cfd5cdcecd2ab0b08fae0e80b3ff35c'),
('not_wednesday','https://i.pinimg.com/736x/79/b7/84/79b784792d35c304af077ee2e450eea1.jpg');

INSERT INTO gifs (category, gif_url) VALUES
('d1','https://media1.tenor.com/m/zohPU51tyjoAAAAC/puppet-talk.gif');

