DELIMITER //

CREATE PROCEDURE CreateBooking(
    IN p_member_id INT,
    IN p_pass_id INT
)
BEGIN

DECLARE slots INT;
DECLARE max_slots INT;

SELECT booked_slots, max_slots
INTO slots, max_slots
FROM training_passes
WHERE pass_id = p_pass_id;

IF slots >= max_slots THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Session is full';
END IF;

INSERT INTO bookings(member_id, pass_id)
VALUES(p_member_id, p_pass_id);

UPDATE training_passes
SET booked_slots = booked_slots + 1
WHERE pass_id = p_pass_id;

END //

DELIMITER ;
