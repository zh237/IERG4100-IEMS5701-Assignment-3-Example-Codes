

function encoded = Encode(data_bits)
    m = length(data_bits);
    r = 0;
    while 2^r < (m + r + 1)
        r = r + 1;
    end
    n = m + r;

    encoded = zeros(1, n);
    j = 1;
    for i = 1:n
        if isPowerOfTwo(i)
            encoded(i) = 0;
        else
            encoded(i) = data_bits(j);
            j = j + 1;
        end
    end
    for i = 0:r-1
        parity_pos = 2^i;
        parity = 0;
        for j = 1:n
            if bitand(j, parity_pos) && j ~= parity_pos
                parity = bitxor(parity, encoded(j));
            end
        end
        encoded(parity_pos) = parity;
    end
end

function corrupted = addErrorToCode(encoded, position)
    corrupted = encoded;
    if position < 1 || position > length(encoded)
        error("Position out of range.");
    end
    corrupted(position) = mod(encoded(position) + 1, 2); % flip
end

function error_pos = checkForError(received)
    n = length(received);
    r = 0;
    while 2^r <= n
        r = r + 1;
    end

    error_pos = 0;
    for i = 0:r-1
        parity_pos = 2^i;
        parity = 0;
        for j = 1:n
            if bitand(j, parity_pos)
                parity = bitxor(parity, received(j));
            end
        end
        if parity ~= 0
            error_pos = error_pos + parity_pos;
        end
    end
end

function data_bits = recoverOriginalMessage(code)
    n = length(code);
    data_bits = [];
    for i = 1:n
        if ~isPowerOfTwo(i)
            data_bits = [data_bits, code(i)];
        end
    end
end

function tf = isPowerOfTwo(x)
    tf = (x > 0) && (bitand(x, x - 1) == 0);
end


%% Main program
data_bits = [1 1 0 1];
fprintf('Original code: ');
disp(data_bits);

encoded = Encode(data_bits);
fprintf('Hamming code: ');
disp(encoded);


received = addErrorToCode(encoded, 7);
fprintf('Received code: ');
disp(received);

error_pos = checkForError(received);

if error_pos == 0
    disp('✅ No error detected.');
    corrected = received;
else
    fprintf('❗ Error detected at position: %d\n', error_pos);
    corrected = received;
    corrected(error_pos) = mod(received(error_pos) + 1, 2); % flip
end

original = recoverOriginalMessage(corrected);
fprintf('Recovered code: ');
disp(original);
